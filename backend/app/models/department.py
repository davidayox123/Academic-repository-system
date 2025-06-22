from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..core.database import Base

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True, name="department_id")
    name = Column(String(255), unique=True, nullable=False, index=True, name="department_name")
    code = Column(String(10), nullable=False, unique=True, index=True)  # e.g., "CS", "ENG"
    faculty = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    head_of_department = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    building = Column(String(100), nullable=True)
    room_number = Column(String(20), nullable=True)
    is_active = Column(String(1), default='1')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Statistics
    total_users = Column(Integer, default=0)
    total_documents = Column(Integer, default=0)
    
    # --- Relationships ---
    # A department has many users
    users = relationship("User", back_populates="department")
    
    # A department has many documents
    documents = relationship("Document", back_populates="department")

    def __repr__(self):
        return f"<Department(id={self.id}, name={self.name}, code={self.code})>"
