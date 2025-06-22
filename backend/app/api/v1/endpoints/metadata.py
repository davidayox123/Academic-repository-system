from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from ....core.database import get_db
from ....models.metadata import Metadata
from ....models.document import Document
from ....schemas.metadata import MetadataCreate, MetadataUpdate, MetadataResponse

router = APIRouter()

@router.get("/{document_id}", response_model=MetadataResponse)
async def get_document_metadata(
    document_id: str,
    db: Session = Depends(get_db)
):
    """Get metadata for a specific document"""
    metadata = db.query(Metadata).filter(Metadata.document_id == document_id).first()
    if not metadata:
        raise HTTPException(status_code=404, detail="Metadata not found")
    return metadata

@router.post("/", response_model=MetadataResponse)
async def create_metadata(
    metadata: MetadataCreate,
    db: Session = Depends(get_db)
):
    """Create metadata for a document"""
    # Check if document exists
    document = db.query(Document).filter(Document.id == metadata.document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check if metadata already exists
    existing = db.query(Metadata).filter(Metadata.document_id == metadata.document_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Metadata already exists for this document")
    
    db_metadata = Metadata(**metadata.dict())
    db.add(db_metadata)
    db.commit()
    db.refresh(db_metadata)
    return db_metadata

@router.put("/{metadata_id}", response_model=MetadataResponse)
async def update_metadata(
    metadata_id: str,
    metadata: MetadataUpdate,
    db: Session = Depends(get_db)
):
    """Update metadata"""
    db_metadata = db.query(Metadata).filter(Metadata.id == metadata_id).first()
    if not db_metadata:
        raise HTTPException(status_code=404, detail="Metadata not found")
    
    update_data = metadata.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_metadata, field, value)
    
    db.commit()
    db.refresh(db_metadata)
    return db_metadata

@router.delete("/{metadata_id}")
async def delete_metadata(
    metadata_id: str,
    db: Session = Depends(get_db)
):
    """Delete metadata"""
    db_metadata = db.query(Metadata).filter(Metadata.id == metadata_id).first()
    if not db_metadata:
        raise HTTPException(status_code=404, detail="Metadata not found")
    
    db.delete(db_metadata)
    db.commit()
    return {"message": "Metadata deleted successfully"}
