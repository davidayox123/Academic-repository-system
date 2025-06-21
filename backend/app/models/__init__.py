# Import all models from their respective files
from .user import User, UserRole
from .document import Document, DocumentStatus, DocumentCategory, DocumentType
from .department import Department
from .review import Review, ReviewDecision, ReviewStatus
from .activity_log import ActivityLog, ActivityType, ActivityLevel
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
    "Review",
    "ReviewDecision", 
    "ReviewStatus",
    "ActivityLog",
    "ActivityType",
    "ActivityLevel",
    "Download"
]
