from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    SUPERVISOR = "supervisor"
    STAFF = "staff"
    STUDENT = "student"

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole
    department_id: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    
    # Student-specific fields
    student_id: Optional[str] = None
    year_of_study: Optional[int] = None
    gpa: Optional[str] = None
    enrollment_date: Optional[date] = None
    graduation_date: Optional[date] = None
    
    # Staff-specific fields
    employee_id: Optional[str] = None
    position: Optional[str] = None
    hire_date: Optional[date] = None
    office_location: Optional[str] = None
    salary: Optional[str] = None
    
    # Supervisor-specific fields
    title: Optional[str] = None
    specialization: Optional[str] = None
    research_interests: Optional[str] = None
    qualifications: Optional[str] = None
    years_of_experience: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = None
    department_id: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    
    # Student-specific fields
    student_id: Optional[str] = None
    year_of_study: Optional[int] = None
    gpa: Optional[str] = None
    enrollment_date: Optional[date] = None
    graduation_date: Optional[date] = None
    
    # Staff-specific fields
    employee_id: Optional[str] = None
    position: Optional[str] = None
    hire_date: Optional[date] = None
    office_location: Optional[str] = None
    salary: Optional[str] = None
    
    # Supervisor-specific fields
    title: Optional[str] = None
    specialization: Optional[str] = None
    research_interests: Optional[str] = None
    qualifications: Optional[str] = None
    years_of_experience: Optional[int] = None

class UserResponse(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserProfile(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    full_name: str  # computed field
    role: UserRole
    department_name: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    
    # Role-specific fields (populated based on role)
    student_id: Optional[str] = None
    year_of_study: Optional[int] = None
    gpa: Optional[str] = None
    enrollment_date: Optional[date] = None
    graduation_date: Optional[date] = None
    
    employee_id: Optional[str] = None
    position: Optional[str] = None
    hire_date: Optional[date] = None
    office_location: Optional[str] = None
    
    title: Optional[str] = None
    specialization: Optional[str] = None
    research_interests: Optional[str] = None
    qualifications: Optional[str] = None
    years_of_experience: Optional[int] = None
    
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class MockUser(BaseModel):
    """Mock user for demo login implementation"""
    id: str
    email: str
    first_name: str
    last_name: str
    full_name: str
    role: UserRole
    department_id: Optional[str] = None
    department_name: Optional[str] = None
