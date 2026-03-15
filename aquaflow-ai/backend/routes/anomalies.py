from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.utils.database import get_db
from backend.models.db_models import Anomaly

router = APIRouter()


@router.get("/")
async def list_anomalies(
    sensor_id: str | None = Query(None),
    severity: str | None = Query(None),
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    q = select(Anomaly).order_by(Anomaly.detected_at.desc()).limit(limit)
    if sensor_id:
        q = q.where(Anomaly.sensor_id == sensor_id)
    if severity:
        q = q.where(Anomaly.severity == severity)
    result = await db.execute(q)
    return result.scalars().all()
