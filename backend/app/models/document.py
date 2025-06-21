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

class Document(Base):
    __tablename__ = "documents"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False, index=True)
    
    # File information
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String(100), nullable=False)
    
    # Status and categorization
    status = Column(Enum(DocumentStatus), default=DocumentStatus.PENDING, index=True)
    
    # Foreign Keys - Required relationships
    uploader_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    department_id = Column(String(36), ForeignKey("departments.id"), nullable=False, index=True)
    supervisor_id = Column(String(36), ForeignKey("users.id"), nullable=True, index=True)
    
    # Rejection handling
    rejection_reason = Column(Text, nullable=True)
    
    # Statistics
    download_count = Column(Integer, default=0)
    
    # Timestamps
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    uploader = relationship("User", foreign_keys=[uploader_id], back_populates="uploaded_documents")
    supervisor = relationship("User", foreign_keys=[supervisor_id], back_populates="supervised_documents")
    department = relationship("Department", back_populates="documents")
      # One-to-one with Metadata
    document_metadata = relationship("Metadata", back_populates="document", uselist=False)
    
    # One-to-many relationships
    reviews = relationship("Review", back_populates="document")
    downloads = relationship("Download", back_populates="document")
    audit_logs = relationship("AuditLog", back_populates="document")

    def __repr__(self):
        return f"<Document(id={self.id}, title={self.title}, status={self.status})>"

    def __repr__(self):
        return f"<Document(id={self.id}, title={self.title}, status={self.status})>"
