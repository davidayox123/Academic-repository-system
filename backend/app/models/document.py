from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import uuid

from ..core.database import Base

class DocumentStatus(str, enum.Enum):
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"

class DocumentCategory(str, enum.Enum):
    RESEARCH = "research"
    THESIS = "thesis"
    ASSIGNMENT = "assignment"
    PRESENTATION = "presentation"
    PAPER = "paper"
    REPORT = "report"
    PROJECT = "project"
    OTHER = "other"

class DocumentType(str, enum.Enum):
    PDF = "pdf"
    DOC = "doc"
    DOCX = "docx"
    PPT = "ppt"
    PPTX = "pptx"
    TXT = "txt"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    ARCHIVE = "archive"

class Document(Base):
    __tablename__ = "documents"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), name="document_id")
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # File information
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String(100), nullable=False)
    file_extension = Column(String(10), nullable=False)
    mime_type = Column(String(100), nullable=False)
    
    # Document metadata
    category = Column(Enum(DocumentCategory, native_enum=False), default=DocumentCategory.OTHER, index=True)
    document_type = Column(Enum(DocumentType, native_enum=False), index=True)
    tags = Column(JSON, nullable=True)  # Store tags as JSON array
    keywords = Column(Text, nullable=True)  # Searchable keywords
    abstract = Column(Text, nullable=True)
    language = Column(String(10), default="en")
    
    # Academic metadata
    course_code = Column(String(20), nullable=True, index=True)
    academic_year = Column(String(20), nullable=True)
    semester = Column(String(20), nullable=True)
    
    # Status and workflow
    status = Column(Enum(DocumentStatus, native_enum=False), default=DocumentStatus.PENDING, index=True)
    is_public = Column(Boolean, default=False, index=True)
    is_featured = Column(Boolean, default=False)
      # Foreign Keys
    uploader_id = Column(CHAR(36), ForeignKey("users.user_id"), nullable=False, index=True)
    department_id = Column(CHAR(36), ForeignKey("departments.department_id"), nullable=False, index=True)
    supervisor_id = Column(CHAR(36), ForeignKey("users.user_id"), nullable=True, index=True)
    
    # Review and approval
    approval_date = Column(DateTime(timezone=True), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    reviewer_comments = Column(Text, nullable=True)
    
    # File processing
    is_processed = Column(Boolean, default=False)
    thumbnail_path = Column(String(500), nullable=True)
    preview_path = Column(String(500), nullable=True)
    text_content = Column(Text, nullable=True)  # Extracted text for search
    
    # Statistics and analytics
    download_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
      # Version control
    version = Column(String(20), default="1.0")
    parent_document_id = Column(CHAR(36), ForeignKey("documents.document_id"), nullable=True)
    
    # Security and access
    access_level = Column(String(20), default="department")  # public, department, private
    download_allowed = Column(Boolean, default=True)
    
    # Timestamps
    upload_date = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    last_accessed = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    uploader = relationship("User", foreign_keys=[uploader_id], back_populates="uploaded_documents")
    supervisor = relationship("User", foreign_keys=[supervisor_id], back_populates="supervised_documents")
    department = relationship("Department", back_populates="documents")
    
    # Version relationships
    parent_document = relationship("Document", remote_side=[id], backref="versions")    # One-to-many relationships
    reviews = relationship("Review", back_populates="document", cascade="all, delete-orphan")
    downloads = relationship("Download", back_populates="document", cascade="all, delete-orphan")
    
    # One-to-one relationship with metadata
    document_metadata = relationship("Metadata", back_populates="document", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Document(id={self.id}, title={self.title}, status={self.status})>"
