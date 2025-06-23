from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..core.database import Base

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True, name="department_id")
    name = Column(String(255), unique=True, nullable=False, index=True, name="department_name")
    faculty = Column(String(255), nullable=False)
    head_of_department = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # --- Relationships ---
    users = relationship("User", back_populates="department", foreign_keys="User.department_id")
    documents = relationship("Document", back_populates="department")

    def __repr__(self):
        return f"<Department(id={self.id}, name={self.name})>"
