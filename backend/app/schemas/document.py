import uuid
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.models.document import DocumentStatus

# This will be the base schema with common fields
class DocumentBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255, example="The Impact of AI on Academic Research")
    supervisor_id: Optional[uuid.UUID] = Field(None, example=uuid.uuid4())

# Schema for the uploader information to be nested in the response
class UploaderInfo(BaseModel):
    id: uuid.UUID
    full_name: str
    email: str

    class Config:
        from_attributes = True

# This is the main response schema for a single document
class DocumentResponse(DocumentBase):
    id: uuid.UUID
    status: DocumentStatus
    upload_date: datetime
    uploader: UploaderInfo
    department_id: uuid.UUID
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    rejection_reason: Optional[str] = None
    download_url: Optional[str] = None # This will be set in the endpoint

    class Config:
        from_attributes = True

# This schema will be used for creating a document record in the DB
# It will be populated from form fields in the endpoint
class DocumentCreate(DocumentBase):
    uploader_id: uuid.UUID
    department_id: uuid.UUID

# This schema is for updating a document
class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[DocumentStatus] = None
    supervisor_id: Optional[uuid.UUID] = None
    rejection_reason: Optional[str] = None

class DocumentFilter(BaseModel):
    status: Optional[DocumentStatus] = None
    department_id: Optional[uuid.UUID] = None
    supervisor_id: Optional[uuid.UUID] = None
    uploader_id: Optional[uuid.UUID] = None
    sort_by: Optional[str] = "upload_date"
    sort_order: Optional[str] = "desc"

# Response for a list of documents
class DocumentListResponse(BaseModel):
    items: List[DocumentResponse]
    total: int

    class Config:
        from_attributes = True
