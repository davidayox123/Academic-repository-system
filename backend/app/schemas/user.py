import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr

# Enum classes must match the definitions in the SQLAlchemy model
class UserRole(str, Enum):
    STUDENT = "student"
    STAFF = "staff"
    SUPERVISOR = "supervisor"
    ADMIN = "admin"

class UserLevel(str, Enum):
    L100 = '100'
    L200 = '200'
    L300 = '300'
    L400 = '400'
    L500 = '500'

class AdminLevel(str, Enum):
    SUPER = 'super'
    DEPARTMENT = 'department'
    LIMITED = 'limited'

# Base User Schema
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    role: UserRole
    department_id: uuid.UUID

# Schema for creating a user
class UserCreate(UserBase):
    password: str
    
    # Role-specific fields are optional during creation
    matric_no: Optional[str] = None
    level: Optional[UserLevel] = None
    staff_id: Optional[str] = None
    position: Optional[str] = None
    office_no: Optional[str] = None
    assigned_department: Optional[uuid.UUID] = None
    specialization_area: Optional[str] = None
    max_documents: Optional[int] = 50
    admin_id: Optional[str] = None
    admin_level: Optional[AdminLevel] = AdminLevel.LIMITED
    permissions_scope: Optional[str] = None

# Schema for updating a user
class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: uuid.UUID
    role: UserRole
    is_active: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserProfile(User):
    department_name: Optional[str] = None
