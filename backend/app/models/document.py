from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum, BIGINT
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import uuid

from ..core.database import Base

class DocumentStatus(str, enum.Enum):
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    UNDER_REVIEW = "under_review"

class Document(Base):
    __tablename__ = "documents"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), name="document_id")
    title = Column(String(255), nullable=False)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(DocumentStatus, native_enum=False), default=DocumentStatus.SUBMITTED)
    uploader_id = Column(CHAR(36), ForeignKey("users.user_id"), nullable=False)
    department_id = Column(CHAR(36), ForeignKey("departments.department_id"), nullable=False)
    supervisor_id = Column(CHAR(36), ForeignKey("users.user_id"), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    file_path = Column(String(500), nullable=True)
    file_size = Column(BIGINT, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    uploader = relationship("User", foreign_keys=[uploader_id], back_populates="uploaded_documents")
    supervisor = relationship("User", foreign_keys=[supervisor_id], back_populates="supervised_documents")
    department = relationship("Department", back_populates="documents")
    
    reviews = relationship("Review", back_populates="document", cascade="all, delete-orphan")
    downloads = relationship("Download", back_populates="document", cascade="all, delete-orphan")
    document_metadata = relationship("Metadata", back_populates="document", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Document(id={self.id}, title={self.title}, status={self.status})>"
