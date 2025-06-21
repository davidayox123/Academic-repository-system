from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import uuid

from ..core.database import Base

class ReviewDecision(enum.Enum):
    APPROVED = "approved"
    REJECTED = "rejected"

class Review(Base):
    __tablename__ = "reviews"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)  # Reviewer (Supervisor)
    
    # Review details
    review_date = Column(DateTime(timezone=True), server_default=func.now())
    comments = Column(Text, nullable=True)
    decision = Column(Enum(ReviewDecision), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    document = relationship("Document", back_populates="reviews")
    reviewer = relationship("User", back_populates="reviews")

    def __repr__(self):
        return f"<Review(id={self.id}, decision={self.decision}, document_id={self.document_id})>"
