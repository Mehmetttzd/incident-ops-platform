from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.audit_log import AuditLog

from app.db.deps import get_db
from app.models.incident import Incident
from app.schemas.incident import IncidentCreate, IncidentOut, IncidentStatusUpdate
from app.services.incidents import change_incident_status

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post("", response_model=IncidentOut)
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db)):
    incident = Incident(title=payload.title, description=payload.description)
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


@router.patch("/{incident_id}/status", response_model=IncidentOut)
def update_status(
    incident_id: int,
    payload: IncidentStatusUpdate,
    db: Session = Depends(get_db),
    x_actor: str | None = Header(default=None),  # optional: pass X-Actor header
):
    incident = db.get(Incident, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    try:
        return change_incident_status(
            db=db,
            incident=incident,
            new_status=payload.status,
            actor=x_actor or "system",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{incident_id}/audit")
def get_audit_trail(incident_id: int, db: Session = Depends(get_db)):
    stmt = (
        select(AuditLog)
        .where(AuditLog.entity_type == "incident", AuditLog.entity_id == incident_id)
        .order_by(AuditLog.created_at.asc())
    )
    return db.execute(stmt).scalars().all()
