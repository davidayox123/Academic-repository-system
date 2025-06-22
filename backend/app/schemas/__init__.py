from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from ..models import UserRole, DocumentStatus, ReviewDecision

# Import all schemas
from .document import DocumentBase, DocumentCreate, DocumentUpdate, DocumentResponse, DocumentListResponse
from .user import UserCreate, UserUpdate, User, UserProfile
from .auth import Token, TokenData, LoginRequest

# Base schemas
class BaseResponse(BaseModel):
    success: bool = True
    message: Optional[str] = None

class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    limit: int
    total_pages: int

# User schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole
    department_id: str

class UserCreate(UserBase):
    password: str
    confirm_password: str
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department_id: Optional[str] = None
    avatar: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: UserRole
    department_id: str
    department_name: Optional[str] = None
    avatar: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserProfile(UserResponse):
    pass

# Authentication schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseResponse):
    data: Optional[dict] = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('New passwords do not match')
        return v

# Department schemas
class DepartmentBase(BaseModel):
    name: str
    faculty: str
    description: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    faculty: Optional[str] = None
    description: Optional[str] = None

class DepartmentResponse(BaseModel):
    id: str
    name: str
    faculty: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Document schemas
class DocumentBase(BaseModel):
    title: str
    description: Optional[str] = None
    keywords: List[str] = []
    authors: List[str] = []
    year: int
    abstract: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(DocumentBase):
    title: Optional[str] = None
    year: Optional[int] = None

class DocumentResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    file_name: str
    file_size: int
    file_type: str
    status: DocumentStatus
    uploader_id: str
    uploader_name: Optional[str] = None
    department_id: str
    department_name: Optional[str] = None
    keywords: List[str] = []
    authors: List[str] = []
    year: int
    abstract: Optional[str] = None
    download_count: int
    approved_at: Optional[datetime] = None
    approved_by: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class DocumentSummary(BaseModel):
    id: str
    title: str
    status: DocumentStatus
    uploader_name: Optional[str] = None
    department_name: Optional[str] = None
    year: int
    download_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Review schemas
class ReviewBase(BaseModel):
    decision: ReviewDecision
    comments: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(ReviewBase):
    pass

class ReviewResponse(BaseModel):
    id: str
    document_id: str
    document_title: Optional[str] = None
    reviewer_id: str
    reviewer_name: Optional[str] = None
    decision: ReviewDecision
    comments: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Audit log schemas
class AuditLogResponse(BaseModel):
    id: str
    user_id: str
    user_name: Optional[str] = None
    document_id: Optional[str] = None
    document_title: Optional[str] = None
    action: str
    details: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Download schemas
class DownloadResponse(BaseModel):
    id: str
    document_id: str
    document_title: Optional[str] = None
    user_id: str
    user_name: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Search schemas
class SearchRequest(BaseModel):
    query: Optional[str] = None
    filters: Optional[dict] = None
    sort_by: Optional[str] = "created_at"
    sort_order: Optional[str] = "desc"
    page: Optional[int] = 1
    limit: Optional[int] = 20

class SearchResponse(BaseModel):
    results: List[DocumentResponse]
    total: int
    page: int
    limit: int
    total_pages: int

# Statistics schemas
class DashboardStats(BaseModel):
    total_documents: int
    pending_reviews: int
    approved_documents: int
    rejected_documents: int
    total_downloads: int
    total_users: int
    recent_activity: List[AuditLogResponse]

class UserStats(BaseModel):
    documents_count: int
    pending_count: int
    approved_count: int
    rejected_count: int
    total_downloads: int
    recent_documents: List[DocumentSummary]

# File upload schemas
class UploadResponse(BaseModel):
    filename: str
    file_size: int
    file_type: str
    file_path: str
    
# Error schemas
class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    details: Optional[dict] = None
