# Import all models from their respective files
from .user import User, UserRole
from .document import Document, DocumentStatus, DocumentCategory

# Make all models available when importing from app.models
__all__ = [
    "User", 
    "UserRole",
    "Document", 
    "DocumentStatus", 
    "DocumentCategory"
]
