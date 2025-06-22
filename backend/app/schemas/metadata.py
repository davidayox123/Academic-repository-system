from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MetadataBase(BaseModel):
    keywords: str  # Comma-separated keywords
    publication_year: int
    authors: str  # Comma-separated authors
    abstract: Optional[str] = None
    subject_area: Optional[str] = None

class MetadataCreate(MetadataBase):
    document_id: str

class MetadataUpdate(BaseModel):
    keywords: Optional[str] = None
    publication_year: Optional[int] = None
    authors: Optional[str] = None
    abstract: Optional[str] = None
    subject_area: Optional[str] = None

class MetadataResponse(MetadataBase):
    id: str
    document_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Helper schemas for processing keywords and authors
class ProcessedMetadata(MetadataResponse):
    keywords_list: List[str] = []
    authors_list: List[str] = []
    
    class Config:
        from_attributes = True
