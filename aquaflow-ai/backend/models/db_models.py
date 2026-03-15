"""
SQLAlchemy ORM models for AquaFlow AI.
"""

from datetime import datetime
from sqlalchemy import String, Float, DateTime, ForeignKey, Enum, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from backend.utils.database import Base


class SeverityLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AnomalyType(str, enum.Enum):
    PRESSURE_HIGH = "pressure_high"
    PRESSURE_LOW = "pressure_low"
    FLOW_SPIKE = "flow_spike"
    FLOW_DROP = "flow_drop"
    LEAK_SUSPECTED = "leak_suspected"
    PIPE_BURST_RISK = "pipe_burst_risk"


class Sensor(Base):
    __tablename__ = "sensors"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    zone: Mapped[str] = mapped_column(String, nullable=False)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    installed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    readings: Mapped[list["SensorReading"]] = relationship(back_populates="sensor")


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sensor_id: Mapped[str] = mapped_column(ForeignKey("sensors.id"), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    flow_rate: Mapped[float] = mapped_column(Float)     # L/min
    pressure: Mapped[float] = mapped_column(Float)      # bar
    temperature: Mapped[float] = mapped_column(Float, nullable=True)   # °C

    sensor: Mapped["Sensor"] = relationship(back_populates="readings")
    anomaly: Mapped["Anomaly"] = relationship(back_populates="reading", uselist=False)


class Anomaly(Base):
    __tablename__ = "anomalies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    reading_id: Mapped[int] = mapped_column(ForeignKey("sensor_readings.id"), nullable=False)
    sensor_id: Mapped[str] = mapped_column(String, nullable=False)
    anomaly_type: Mapped[AnomalyType] = mapped_column(Enum(AnomalyType))
    severity: Mapped[SeverityLevel] = mapped_column(Enum(SeverityLevel))
    score: Mapped[float] = mapped_column(Float)         # anomaly score 0–1
    detected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    reading: Mapped["SensorReading"] = relationship(back_populates="anomaly")
    alert: Mapped["Alert"] = relationship(back_populates="anomaly", uselist=False)


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    anomaly_id: Mapped[int] = mapped_column(ForeignKey("anomalies.id"), nullable=False)
    sensor_id: Mapped[str] = mapped_column(String, nullable=False)
    message: Mapped[str] = mapped_column(Text)
    severity: Mapped[SeverityLevel] = mapped_column(Enum(SeverityLevel))
    is_acknowledged: Mapped[bool] = mapped_column(Boolean, default=False)
    acknowledged_by: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    acknowledged_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    anomaly: Mapped["Anomaly"] = relationship(back_populates="alert")
