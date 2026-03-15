from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.utils.database import get_db
from backend.models.db_models import Sensor, SensorReading
from backend.services.ingestion import ingest_reading

router = APIRouter()


# ── Schemas ──────────────────────────────────────────────────────────────────

class SensorCreate(BaseModel):
    id: str
    name: str
    zone: str
    latitude: float
    longitude: float


class ReadingIngest(BaseModel):
    flow_rate: float
    pressure: float
    temperature: float | None = None
    timestamp: datetime | None = None


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/")
async def list_sensors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Sensor))
    sensors = result.scalars().all()
    return sensors


@router.post("/", status_code=201)
async def create_sensor(payload: SensorCreate, db: AsyncSession = Depends(get_db)):
    sensor = Sensor(**payload.model_dump())
    db.add(sensor)
    await db.commit()
    await db.refresh(sensor)
    return sensor


@router.get("/{sensor_id}")
async def get_sensor(sensor_id: str, db: AsyncSession = Depends(get_db)):
    sensor = await db.get(Sensor, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor


@router.get("/{sensor_id}/readings")
async def get_readings(
    sensor_id: str,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(SensorReading)
        .where(SensorReading.sensor_id == sensor_id)
        .order_by(SensorReading.timestamp.desc())
        .limit(limit)
    )
    return result.scalars().all()


@router.post("/{sensor_id}/readings", status_code=201)
async def ingest(
    sensor_id: str,
    payload: ReadingIngest,
    db: AsyncSession = Depends(get_db),
):
    sensor = await db.get(Sensor, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    result = await ingest_reading(
        db=db,
        sensor_id=sensor_id,
        flow_rate=payload.flow_rate,
        pressure=payload.pressure,
        temperature=payload.temperature,
        timestamp=payload.timestamp,
    )
    return result
