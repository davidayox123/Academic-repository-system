from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ..core.database import Base

class Download(Base):
    __tablename__ = "downloads"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), name="download_id")
    document_id = Column(CHAR(36), ForeignKey("documents.document_id"), nullable=False, index=True)
    user_id = Column(CHAR(36), ForeignKey("users.user_id"), nullable=False, index=True)
    download_timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    document = relationship("Document", back_populates="downloads")
    user = relationship("User", back_populates="downloads")

    def __repr__(self):
        return f"<Download(id={self.id}, document_id={self.document_id}, user_id={self.user_id})>"
