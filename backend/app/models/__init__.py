# Import all models from their respective files
from .user import User, UserRole
from .document import Document, DocumentStatus, DocumentCategory, DocumentType
from .department import Department
from .metadata import Metadata
from .review import Review, ReviewDecision, ReviewStatus
from .audit_log import AuditLog
from .download import Download

# Make all models available when importing from app.models
__all__ = [
    "User", 
    "UserRole",
    "Document", 
    "DocumentStatus", 
    "DocumentCategory",
    "DocumentType",
    "Department",
    "Metadata",
    "Review",
    "ReviewDecision", 
    "ReviewStatus",
    "AuditLog",
    "Download"
]
