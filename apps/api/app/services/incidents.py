from sqlalchemy.orm import Session

from app.models.incident import Incident, IncidentStatus
from app.models.audit_log import AuditLog


ALLOWED_TRANSITIONS: dict[IncidentStatus, set[IncidentStatus]] = {
    IncidentStatus.OPEN: {IncidentStatus.ACKNOWLEDGED},
    IncidentStatus.ACKNOWLEDGED: {IncidentStatus.IN_PROGRESS, IncidentStatus.RESOLVED},
    IncidentStatus.IN_PROGRESS: {IncidentStatus.RESOLVED},
    IncidentStatus.RESOLVED: {IncidentStatus.CLOSED, IncidentStatus.IN_PROGRESS},  # allow reopen to in_progress
    IncidentStatus.CLOSED: set(),  # final
}


def assert_can_transition(old: IncidentStatus, new: IncidentStatus) -> None:
    if new == old:
        return
    allowed = ALLOWED_TRANSITIONS.get(old, set())
    if new not in allowed:
        raise ValueError(f"Invalid transition: {old.value} -> {new.value}")


def change_incident_status(
    db: Session,
    incident: Incident,
    new_status: IncidentStatus,
    actor: str = "system",
) -> Incident:
    old_status = incident.status
    assert_can_transition(old_status, new_status)

    if new_status == old_status:
        return incident

    incident.status = new_status

    db.add(
        AuditLog(
            entity_type="incident",
            entity_id=incident.id,
            action="status_change",
            field="status",
            old_value=old_status.value if old_status else None,
            new_value=new_status.value if new_status else None,
            actor=actor,
        )
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident
