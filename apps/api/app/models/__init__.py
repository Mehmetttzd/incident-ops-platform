# Import models so SQLAlchemy registers them on Base.metadata
from app.models.incident import Incident  # noqa: F401
from app.models.audit_log import AuditLog  # noqa: F401
