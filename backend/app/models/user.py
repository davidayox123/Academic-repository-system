from sqlalchemy import Column, String, Boolean, DateTime, Enum, ForeignKey, Integer, Text
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
    middle_name = Column(String(100), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    
    # Role and Department
    role = Column(Enum(UserRole), default=UserRole.STUDENT, index=True)
    department_id = Column(String(36), ForeignKey("departments.id"), nullable=False, index=True)
    
    # Student specific attributes
    matric_no = Column(String(50), nullable=True, index=True)  # For students
    level = Column(Integer, nullable=True)  # For students
    
    # Staff specific attributes  
    staff_id = Column(String(50), nullable=True, index=True)  # For staff
    position = Column(String(100), nullable=True)  # For staff
    office_no = Column(String(50), nullable=True)  # For staff
    
    # Supervisor specific attributes
    assigned_department = Column(String(36), ForeignKey("departments.id"), nullable=True)  # For supervisors
    specialization_area = Column(String(255), nullable=True)  # For supervisors
    max_documents = Column(Integer, nullable=True, default=50)  # For supervisors
    
    # Admin specific attributes
    admin_id = Column(String(50), nullable=True, index=True)  # For admins
    admin_level = Column(Integer, nullable=True, default=1)  # For admins
    permissions_scope = Column(Text, nullable=True)  # For admins (JSON string)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    department = relationship("Department", foreign_keys=[department_id], back_populates="users")
    supervisor_department = relationship("Department", foreign_keys=[assigned_department])
    
    # Document relationships
    uploaded_documents = relationship("Document", foreign_keys="Document.uploader_id", back_populates="uploader")
    supervised_documents = relationship("Document", foreign_keys="Document.supervisor_id", back_populates="supervisor")
    
    # Other relationships
    reviews = relationship("Review", back_populates="reviewer")
    audit_logs = relationship("AuditLog", back_populates="user")
    downloads = relationship("Download", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
