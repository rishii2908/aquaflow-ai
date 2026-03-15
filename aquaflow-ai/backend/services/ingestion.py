"""
Sensor ingestion service — processes incoming readings, runs anomaly detection,
and creates alerts when anomalies are found.
"""

from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.models.db_models import Sensor, SensorReading, Anomaly, Alert, AnomalyType, SeverityLevel
from backend.models.anomaly_detector import detector
from backend.utils.config import settings


async def get_last_reading(db: AsyncSession, sensor_id: str) -> SensorReading | None:
    result = await db.execute(
        select(SensorReading)
        .where(SensorReading.sensor_id == sensor_id)
        .order_by(SensorReading.timestamp.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def ingest_reading(
    db: AsyncSession,
    sensor_id: str,
    flow_rate: float,
    pressure: float,
    temperature: float | None = None,
    timestamp: datetime | None = None,
) -> dict:
    """
    Persist a sensor reading and run anomaly detection.
    Returns a dict with reading_id and any anomaly/alert created.
    """

    ts = timestamp or datetime.utcnow()

    # Compute delta pressure vs last reading
    last = await get_last_reading(db, sensor_id)
    delta_pressure = 0.0
    if last:
        delta_pressure = pressure - last.pressure

    # Persist reading
    reading = SensorReading(
        sensor_id=sensor_id,
        timestamp=ts,
        flow_rate=flow_rate,
        pressure=pressure,
        temperature=temperature,
    )
    db.add(reading)
    await db.flush()

    # Run anomaly detection
    result = detector.predict(
        flow_rate=flow_rate,
        pressure=pressure,
        delta_pressure=delta_pressure,
        hour_of_day=ts.hour,
        day_of_week=ts.weekday(),
    )

    anomaly_id = None
    alert_id = None

    if result.is_anomaly:
        anomaly = Anomaly(
            reading_id=reading.id,
            sensor_id=sensor_id,
            anomaly_type=AnomalyType(result.anomaly_type),
            severity=SeverityLevel(result.severity),
            score=result.score,
            detected_at=ts,
            description=result.description,
        )
        db.add(anomaly)
        await db.flush()
        anomaly_id = anomaly.id

        # Create alert for medium severity and above
        if result.severity in ("medium", "high", "critical"):
            alert = Alert(
                anomaly_id=anomaly.id,
                sensor_id=sensor_id,
                message=f"[{result.severity.upper()}] Sensor {sensor_id}: {result.description}",
                severity=SeverityLevel(result.severity),
            )
            db.add(alert)
            await db.flush()
            alert_id = alert.id

    await db.commit()

    return {
        "reading_id": reading.id,
        "anomaly_detected": result.is_anomaly,
        "anomaly_id": anomaly_id,
        "alert_id": alert_id,
        "anomaly_score": result.score,
        "anomaly_type": result.anomaly_type,
        "severity": result.severity,
    }
