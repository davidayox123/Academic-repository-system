from sqlalchemy import Column, String, Boolean, DateTime, Enum, ForeignKey, Integer, Text, Date
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
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), name="user_id")
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole, native_enum=False), default=UserRole.STUDENT, index=True)
    department_id = Column(CHAR(36), ForeignKey("departments.department_id"), nullable=False, index=True)
    is_active = Column(Boolean, default=True, index=True)

    # Student attributes
    matric_no = Column(String(50), unique=True, index=True)
    level = Column(Enum('100', '200', '300', '400', '500'), nullable=True)

    # Staff attributes
    staff_id = Column(String(50), unique=True, index=True)
    position = Column(String(100), nullable=True)
    office_no = Column(String(20), nullable=True)

    # Supervisor attributes
    assigned_department = Column(CHAR(36), ForeignKey("departments.department_id"), nullable=True)
    specialization_area = Column(Text, nullable=True)
    max_documents = Column(Integer, default=50)

    # Admin attributes
    admin_id = Column(String(50), unique=True, index=True)
    admin_level = Column(Enum('super', 'department', 'limited'), default='limited')
    permissions_scope = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # --- Relationships ---
    # A user belongs to one department
    department = relationship("Department", back_populates="users", foreign_keys=[department_id])

    # A user can upload many documents
    uploaded_documents = relationship("Document", back_populates="uploader", foreign_keys="Document.uploader_id")

    # A supervisor can supervise many documents
    supervised_documents = relationship("Document", back_populates="supervisor", foreign_keys="Document.supervisor_id")
    
    # A user can write many reviews
    reviews = relationship("Review", back_populates="reviewer")

    # A user can have many downloads
    downloads = relationship("Download", back_populates="user")

    @property
    def full_name(self):
        """Return the full name of the user"""
        return f"{self.first_name} {self.last_name}"

    @property
    def name(self):
        """Alias for full_name for backward compatibility"""
        return self.full_name

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
