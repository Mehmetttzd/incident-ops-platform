from datetime import datetime
from pydantic import BaseModel
from app.models.incident import IncidentStatus


class IncidentCreate(BaseModel):
    title: str
    description: str | None = None


class IncidentStatusUpdate(BaseModel):
    status: IncidentStatus


class IncidentOut(BaseModel):
    id: int
    title: str
    description: str | None
    status: IncidentStatus
    created_at: datetime

    model_config = {"from_attributes": True}
