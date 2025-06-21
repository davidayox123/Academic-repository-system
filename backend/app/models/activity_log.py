from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import uuid

from ..core.database import Base

class ActivityType(str, enum.Enum):
    # Document activities
    DOCUMENT_UPLOADED = "document_uploaded"
    DOCUMENT_UPDATED = "document_updated"
    DOCUMENT_DELETED = "document_deleted"
    DOCUMENT_DOWNLOADED = "document_downloaded"
    DOCUMENT_VIEWED = "document_viewed"
    DOCUMENT_SHARED = "document_shared"
    
    # Review activities
    REVIEW_ASSIGNED = "review_assigned"
    REVIEW_STARTED = "review_started"
    REVIEW_COMPLETED = "review_completed"
    DOCUMENT_APPROVED = "document_approved"
    DOCUMENT_REJECTED = "document_rejected"
    
    # User activities
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    USER_REGISTERED = "user_registered"
    PROFILE_UPDATED = "profile_updated"
    
    # System activities
    SYSTEM_BACKUP = "system_backup"
    SYSTEM_MAINTENANCE = "system_maintenance"

class ActivityLevel(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Activity details
    activity_type = Column(Enum(ActivityType, native_enum=False), nullable=False, index=True)
    activity_level = Column(Enum(ActivityLevel, native_enum=False), default=ActivityLevel.INFO, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Related entities
    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=True, index=True)
    document_id = Column(CHAR(36), ForeignKey("documents.id"), nullable=True, index=True)
    department_id = Column(CHAR(36), ForeignKey("departments.id"), nullable=True, index=True)
    
    # Additional data
    metadata = Column(JSON, nullable=True)  # Store additional context as JSON
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    user_agent = Column(String(500), nullable=True)
    
    # Categorization
    category = Column(String(50), nullable=True, index=True)  # academic, administrative, technical
    tags = Column(JSON, nullable=True)  # Store tags as JSON array
    
    # Visibility and notifications
    is_public = Column(String(1), default='0')  # Public in activity feed
    is_notification = Column(String(1), default='0')  # Should trigger notification
    notification_sent = Column(String(1), default='0')  # Has notification been sent
    
    # Timestamps
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="activity_logs")
    document = relationship("Document", back_populates="activity_logs")
    department = relationship("Department")

    def __repr__(self):
        return f"<ActivityLog(id={self.id}, type={self.activity_type}, user_id={self.user_id})>"
