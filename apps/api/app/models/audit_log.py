from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)

    entity_type: Mapped[str] = mapped_column(String(50))  # e.g. "incident"
    entity_id: Mapped[int] = mapped_column(Integer)

    action: Mapped[str] = mapped_column(String(50))  # e.g. "status_change"
    field: Mapped[str] = mapped_column(String(50))   # e.g. "status"

    old_value: Mapped[str | None] = mapped_column(Text)
    new_value: Mapped[str | None] = mapped_column(Text)

    actor: Mapped[str] = mapped_column(String(100), default="system")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
