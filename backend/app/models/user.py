from sqlalchemy import Column, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import uuid

from ..core.database import Base

class UserRole(enum.Enum):
    STUDENT = "student"
    STAFF = "staff"
    SUPERVISOR = "supervisor"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
      # Profile information
    role = Column(Enum(UserRole), default=UserRole.STUDENT, index=True)
    department_id = Column(String(36), ForeignKey("departments.id"), nullable=False, index=True)
    student_id = Column(String(50), nullable=True, index=True)
      # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    documents = relationship("Document", foreign_keys="Document.uploaded_by", back_populates="uploader")
    
    # Timestamps    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    department = relationship("Department", back_populates="users")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
