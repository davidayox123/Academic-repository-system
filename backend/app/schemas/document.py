from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class DocumentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    category: str = Field(..., min_length=1, max_length=100)
    tags: Optional[List[str]] = Field(default_factory=list)
    department: Optional[str] = Field(None, max_length=100)
    course_code: Optional[str] = Field(None, max_length=20)

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    tags: Optional[List[str]] = None
    department: Optional[str] = Field(None, max_length=100)
    course_code: Optional[str] = Field(None, max_length=20)

class DocumentResponse(DocumentBase):
    id: str
    filename: str
    file_size: Optional[int]
    file_type: str
    status: str
    uploaded_by: str
    reviewed_by: Optional[str] = None
    review_comments: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    download_url: str

    class Config:
        from_attributes = True

class DocumentListResponse(BaseModel):
    documents: List[DocumentResponse]
    total: int
    page: int
    pages: int
    per_page: int
