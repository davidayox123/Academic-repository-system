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
    last_name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole, native_enum=False), default=UserRole.STUDENT, index=True)
    department_id = Column(CHAR(36), ForeignKey("departments.department_id"), nullable=False, index=True)
    avatar = Column(String(500), nullable=True)
    phone = Column(String(20), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    address = Column(Text, nullable=True)
    
    # Student-specific fields
    student_id = Column(String(20), nullable=True, unique=True, index=True)
    year_of_study = Column(Integer, nullable=True)
    gpa = Column(String(10), nullable=True)
    enrollment_date = Column(Date, nullable=True)
    graduation_date = Column(Date, nullable=True)
    
    # Staff-specific fields
    employee_id = Column(String(20), nullable=True, unique=True, index=True)
    position = Column(String(100), nullable=True)
    hire_date = Column(Date, nullable=True)
    office_location = Column(String(100), nullable=True)
    salary = Column(String(20), nullable=True)
      # Supervisor-specific fields
    title = Column(String(100), nullable=True)
    specialization = Column(String(200), nullable=True)
    research_interests = Column(Text, nullable=True)
    qualifications = Column(Text, nullable=True)
    years_of_experience = Column(Integer, nullable=True)
    
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())    # --- Relationships ---
    # A user belongs to one department
    department = relationship("Department", back_populates="users")

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
