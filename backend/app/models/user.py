from sqlalchemy import Column, String, Boolean, DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import uuid

from ..core.database import Base

class UserRole(str, enum.Enum):
    STUDENT = "student"
    STAFF = "staff"
    SUPERVISOR = "supervisor"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole, native_enum=False), default=UserRole.STUDENT, index=True)
    department_id = Column(CHAR(36), ForeignKey("departments.id"), nullable=False, index=True)
    avatar = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # --- Relationships ---
    # A user belongs to one department
    department = relationship("Department", back_populates="users")

    # A user can upload many documents
    uploaded_documents = relationship("Document", back_populates="uploader", foreign_keys="Document.uploader_id")

    # A supervisor can supervise many documents
    supervised_documents = relationship("Document", back_populates="supervisor", foreign_keys="Document.supervisor_id")    # A user can write many reviews
    reviews = relationship("Review", back_populates="reviewer")

    # A user can have many activity logs
    activity_logs = relationship("ActivityLog", back_populates="user")

    # A user can have many downloads
    downloads = relationship("Download", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
