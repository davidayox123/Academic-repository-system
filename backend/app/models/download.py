from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..core.database import Base

class Download(Base):
    __tablename__ = "downloads"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Keys
    document_id = Column(CHAR(36), ForeignKey("documents.id"), nullable=False, index=True)
    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False, index=True)
    
    # Download details
    download_date = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    user_agent = Column(String(500), nullable=True)
    file_size_at_download = Column(Integer, nullable=True)  # File size when downloaded
    
    # Download success tracking
    is_successful = Column(String(1), default='1')  # '1' = success, '0' = failed
    error_message = Column(String(255), nullable=True)
    
    # Referrer tracking
    referrer = Column(String(500), nullable=True)
    download_source = Column(String(100), nullable=True)  # web, api, mobile
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    document = relationship("Document", back_populates="downloads")
    user = relationship("User", back_populates="downloads")

    def __repr__(self):
        return f"<Download(id={self.id}, document_id={self.document_id}, user_id={self.user_id})>"
