from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta

from backend.utils.database import get_db
from backend.models.db_models import Anomaly, Alert, SensorReading, Sensor

router = APIRouter()


@router.get("/summary")
async def summary(db: AsyncSession = Depends(get_db)):
    since = datetime.utcnow() - timedelta(hours=24)

    total_sensors = (await db.execute(select(func.count()).select_from(Sensor))).scalar()
    active_sensors = (await db.execute(
        select(func.count()).select_from(Sensor).where(Sensor.is_active == True)  # noqa: E712
    )).scalar()
    readings_24h = (await db.execute(
        select(func.count()).select_from(SensorReading).where(SensorReading.timestamp >= since)
    )).scalar()
    anomalies_24h = (await db.execute(
        select(func.count()).select_from(Anomaly).where(Anomaly.detected_at >= since)
    )).scalar()
    open_alerts = (await db.execute(
        select(func.count()).select_from(Alert).where(Alert.is_acknowledged == False)  # noqa: E712
    )).scalar()
    critical_alerts = (await db.execute(
        select(func.count()).select_from(Alert).where(
            Alert.is_acknowledged == False,  # noqa: E712
            Alert.severity == "critical",
        )
    )).scalar()

    return {
        "generated_at": datetime.utcnow().isoformat(),
        "period_hours": 24,
        "total_sensors": total_sensors,
        "active_sensors": active_sensors,
        "readings_last_24h": readings_24h,
        "anomalies_last_24h": anomalies_24h,
        "open_alerts": open_alerts,
        "critical_alerts": critical_alerts,
    }
