from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    SUPERVISOR = "supervisor"
    STAFF = "staff"
    STUDENT = "student"

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole
    department_id: Optional[str] = None
    phone_number: Optional[str] = None
    status: UserStatus = UserStatus.ACTIVE

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    department_id: Optional[str] = None
    phone_number: Optional[str] = None
    status: Optional[UserStatus] = None

class UserResponse(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserProfile(BaseModel):
    id: str
    email: str
    full_name: str
    role: UserRole
    department_name: Optional[str] = None
    phone_number: Optional[str] = None
    status: UserStatus
    created_at: datetime
    
    class Config:
        from_attributes = True

class MockUser(BaseModel):
    """Mock user for no-auth implementation"""
    id: str
    email: str
    full_name: str
    role: UserRole
    department_id: Optional[str] = None
    department_name: Optional[str] = None
