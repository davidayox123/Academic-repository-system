from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import uuid

from ..core.database import Base

class DocumentStatus(enum.Enum):
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"

class DocumentCategory(enum.Enum):
    RESEARCH = "research"
    THESIS = "thesis"
    ASSIGNMENT = "assignment"
    PRESENTATION = "presentation"
    PAPER = "paper"
    REPORT = "report"
    PROJECT = "project"
    OTHER = "other"

class ReviewDecision(enum.Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    PENDING = "pending"

class Document(Base):
    __tablename__ = "documents"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String(100), nullable=False)
      # Status and categorization
    status = Column(Enum(DocumentStatus), default=DocumentStatus.PENDING, index=True)
    category = Column(Enum(DocumentCategory), default=DocumentCategory.OTHER, index=True)
    department_id = Column(String(36), ForeignKey("departments.id"), nullable=True, index=True)
    course_code = Column(String(20), nullable=True, index=True)
    
    # Metadata
    tags = Column(Text)  # JSON string of tags
    version = Column(Integer, default=1)
      # Statistics
    download_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    
    # Relationships
    uploaded_by = Column(CHAR(36), ForeignKey("users.id"), nullable=False, index=True)
    reviewed_by = Column(CHAR(36), ForeignKey("users.id"), nullable=True, index=True)
    uploader = relationship("User", foreign_keys=[uploaded_by], back_populates="documents")
    reviewer = relationship("User", foreign_keys=[reviewed_by])
      # Review fields
    review_comments = Column(Text, nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
      # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    department = relationship("Department", back_populates="documents")

    def __repr__(self):
        return f"<Document(id={self.id}, title={self.title}, status={self.status})>"
