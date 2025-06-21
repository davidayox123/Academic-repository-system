from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..core.database import Base

class Metadata(Base):
    __tablename__ = "metadata"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False, unique=True, index=True)
    
    # Metadata fields as per specification
    keywords = Column(Text, nullable=False)  # Comma-separated or JSON
    publication_year = Column(Integer, nullable=False, index=True)
    authors = Column(Text, nullable=False)  # Comma-separated or JSON
    
    # Additional metadata
    abstract = Column(Text, nullable=True)
    subject_area = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    document = relationship("Document", back_populates="metadata")

    def __repr__(self):
        return f"<Metadata(id={self.id}, document_id={self.document_id}, year={self.publication_year})>"
