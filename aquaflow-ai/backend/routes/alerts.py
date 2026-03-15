from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.utils.database import get_db
from backend.models.db_models import Alert

router = APIRouter()


class AcknowledgePayload(BaseModel):
    operator_name: str


@router.get("/")
async def list_alerts(
    unacknowledged_only: bool = False,
    db: AsyncSession = Depends(get_db),
):
    q = select(Alert).order_by(Alert.created_at.desc())
    if unacknowledged_only:
        q = q.where(Alert.is_acknowledged == False)  # noqa: E712
    result = await db.execute(q)
    return result.scalars().all()


@router.post("/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: int,
    payload: AcknowledgePayload,
    db: AsyncSession = Depends(get_db),
):
    alert = await db.get(Alert, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    if alert.is_acknowledged:
        raise HTTPException(status_code=400, detail="Alert already acknowledged")

    alert.is_acknowledged = True
    alert.acknowledged_by = payload.operator_name
    alert.acknowledged_at = datetime.utcnow()
    await db.commit()
    await db.refresh(alert)
    return alert
