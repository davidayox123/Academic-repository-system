from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum, Integer
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import uuid

from ..core.database import Base

class ReviewStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class ReviewDecision(str, enum.Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"

class Review(Base):
    __tablename__ = "reviews"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Keys
    document_id = Column(CHAR(36), ForeignKey("documents.id"), nullable=False, index=True)
    reviewer_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False, index=True)
    
    # Review content
    status = Column(Enum(ReviewStatus, native_enum=False), default=ReviewStatus.PENDING, index=True)
    decision = Column(Enum(ReviewDecision, native_enum=False), nullable=True, index=True)
    comments = Column(Text, nullable=True)
    feedback = Column(Text, nullable=True)
    suggestions = Column(Text, nullable=True)
    
    # Rating system (1-5 stars)
    rating_quality = Column(Integer, nullable=True)  # 1-5
    rating_relevance = Column(Integer, nullable=True)  # 1-5
    rating_originality = Column(Integer, nullable=True)  # 1-5
    overall_rating = Column(Integer, nullable=True)  # 1-5
    
    # Review process
    assigned_date = Column(DateTime(timezone=True), server_default=func.now())
    started_date = Column(DateTime(timezone=True), nullable=True)
    completed_date = Column(DateTime(timezone=True), nullable=True)
    
    # Metadata
    priority = Column(String(20), default="normal")  # low, normal, high, urgent
    estimated_hours = Column(Integer, nullable=True)
    actual_hours = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    document = relationship("Document", back_populates="reviews")
    reviewer = relationship("User", back_populates="reviews")

    def __repr__(self):
        return f"<Review(id={self.id}, document_id={self.document_id}, status={self.status})>"
