from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
import shutil
from pathlib import Path
from datetime import datetime
import json

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentResponse, DocumentUpdate
from .websocket import notify_document_uploaded, notify_activity_update

router = APIRouter()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path(__file__).parent.parent.parent.parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# Allowed file types
ALLOWED_EXTENSIONS = {
    '.pdf', '.doc', '.docx', '.txt', '.md', '.tex', 
    '.ppt', '.pptx', '.xls', '.xlsx', '.csv',
    '.png', '.jpg', '.jpeg', '.gif', '.svg'
}

def validate_file_type(filename: str) -> bool:
    """Validate if file type is allowed"""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

def get_file_size_mb(file_size: int) -> float:
    """Convert file size to MB"""
    return file_size / (1024 * 1024)

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    category: str = Form(...),
    tags: Optional[str] = Form(None),
    department: Optional[str] = Form(None),
    course_code: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload a new document"""
    
    # Validate file type
    if not validate_file_type(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Check file size (max 50MB)
    if file.size and get_file_size_mb(file.size) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size too large. Maximum size is 50MB"
        )
    
    try:
        # Generate unique filename
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Save file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
          # Parse tags
        tag_list = [tag.strip() for tag in tags.split(',')] if tags else []
        
        # Create document record
        document = Document(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            category=category,
            tags=json.dumps(tag_list),  # Store tags as JSON string
            department=department,
            course_code=course_code,
            filename=file.filename,
            file_path=str(file_path),
            file_size=file.size,
            file_type=file_extension,
            uploaded_by=current_user.id,
            status="pending",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        # Send WebSocket notification
        try:
            await notify_document_uploaded(current_user.id, {
                "id": document.id,
                "title": document.title,
                "category": document.category,
                "status": document.status
            })
            
            # Also notify activity
            await notify_activity_update({
                "type": "document_uploaded",
                "user": current_user.full_name or current_user.email,
                "document": document.title,
                "timestamp": document.created_at.isoformat()
            })
        except Exception as e:
            # Log error but don't fail the upload
            print(f"WebSocket notification error: {e}")
        
        return DocumentResponse(
            id=document.id,
            title=document.title,
            description=document.description,
            category=document.category,
            tags=tag_list,
            department=document.department,
            course_code=document.course_code,
            filename=document.filename,
            file_size=document.file_size,
            file_type=document.file_type,
            status=document.status,
            uploaded_by=document.uploaded_by,
            reviewed_by=document.reviewed_by,
            created_at=document.created_at,
            updated_at=document.updated_at,
            download_url=f"/api/v1/documents/{document.id}/download"
        )
        
    except Exception as e:
        # Clean up file if document creation fails
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload document: {str(e)}"
        )

@router.post("/upload-batch", response_model=List[DocumentResponse])
async def upload_documents_batch(
    files: List[UploadFile] = File(...),
    titles: List[str] = Form(...),
    descriptions: List[Optional[str]] = Form([]),
    categories: List[str] = Form(...),
    tags_list: List[Optional[str]] = Form([]),
    departments: List[Optional[str]] = Form([]),
    course_codes: List[Optional[str]] = Form([]),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload multiple documents at once"""
    
    if len(files) != len(titles) or len(files) != len(categories):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Number of files must match number of titles and categories"
        )
    
    # Pad shorter lists with None values
    descriptions = descriptions + [None] * (len(files) - len(descriptions))
    tags_list = tags_list + [None] * (len(files) - len(tags_list))
    departments = departments + [None] * (len(files) - len(departments))
    course_codes = course_codes + [None] * (len(files) - len(course_codes))
    
    uploaded_documents = []
    failed_uploads = []
    
    for i, file in enumerate(files):
        try:
            # Validate file type
            if not validate_file_type(file.filename):
                failed_uploads.append(f"{file.filename}: File type not allowed")
                continue
            
            # Check file size
            if file.size and get_file_size_mb(file.size) > 50:
                failed_uploads.append(f"{file.filename}: File size too large (max 50MB)")
                continue
            
            # Generate unique filename
            file_extension = Path(file.filename).suffix
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = UPLOAD_DIR / unique_filename
            
            # Save file to disk
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Parse tags
            tag_list = [tag.strip() for tag in tags_list[i].split(',')] if tags_list[i] else []
            
            # Create document record
            document = Document(
                id=str(uuid.uuid4()),
                title=titles[i],
                description=descriptions[i],
                category=categories[i],
                tags=tag_list,
                department=departments[i],
                course_code=course_codes[i],
                filename=file.filename,
                file_path=str(file_path),
                file_size=file.size,
                file_type=file_extension,
                uploaded_by=current_user.id,
                status="pending",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.add(document)
            db.commit()
            db.refresh(document)
            
            uploaded_documents.append(DocumentResponse(
                id=document.id,
                title=document.title,
                description=document.description,
                category=document.category,
                tags=document.tags,
                department=document.department,
                course_code=document.course_code,
                filename=document.filename,
                file_size=document.file_size,
                file_type=document.file_type,
                status=document.status,
                uploaded_by=document.uploaded_by,
                reviewed_by=document.reviewed_by,
                created_at=document.created_at,
                updated_at=document.updated_at,
                download_url=f"/api/v1/documents/{document.id}/download"
            ))
            
        except Exception as e:
            failed_uploads.append(f"{file.filename}: {str(e)}")
            # Clean up file if document creation fails
            if 'file_path' in locals() and file_path.exists():
                file_path.unlink()
    
    if failed_uploads and not uploaded_documents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"All uploads failed: {'; '.join(failed_uploads)}"
        )
    
    return uploaded_documents

@router.get("/", response_model=List[DocumentResponse])
async def get_documents(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of documents with filtering and pagination"""
    
    query = db.query(Document)
    
    # Filter by user role
    if current_user.role == "student":
        query = query.filter(Document.uploaded_by == current_user.id)
    elif current_user.role == "staff":
        query = query.filter(
            (Document.uploaded_by == current_user.id) | 
            (Document.department == current_user.department)
        )
    # Supervisors and admins can see all documents
    
    # Apply filters
    if category:
        query = query.filter(Document.category == category)
    if status:
        query = query.filter(Document.status == status)
    if search:
        query = query.filter(
            (Document.title.ilike(f"%{search}%")) |
            (Document.description.ilike(f"%{search}%"))
        )
    
    # Apply pagination
    documents = query.order_by(Document.created_at.desc()).offset(skip).limit(limit).all()
    
    return [
        DocumentResponse(
            id=doc.id,
            title=doc.title,
            description=doc.description,
            category=doc.category,
            tags=doc.tags,
            department=doc.department,
            course_code=doc.course_code,
            filename=doc.filename,
            file_size=doc.file_size,
            file_type=doc.file_type,
            status=doc.status,
            uploaded_by=doc.uploaded_by,
            reviewed_by=doc.reviewed_by,
            created_at=doc.created_at,
            updated_at=doc.updated_at,
            download_url=f"/api/v1/documents/{doc.id}/download"
        )
        for doc in documents
    ]

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific document by ID"""
    
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Check access permissions
    if (current_user.role == "student" and document.uploaded_by != current_user.id) or \
       (current_user.role == "staff" and document.uploaded_by != current_user.id and 
        document.department != current_user.department):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return DocumentResponse(
        id=document.id,
        title=document.title,
        description=document.description,
        category=document.category,
        tags=document.tags,
        department=document.department,
        course_code=document.course_code,
        filename=document.filename,
        file_size=document.file_size,
        file_type=document.file_type,
        status=document.status,
        uploaded_by=document.uploaded_by,
        reviewed_by=document.reviewed_by,
        created_at=document.created_at,
        updated_at=document.updated_at,
        download_url=f"/api/v1/documents/{document.id}/download"
    )

@router.get("/{document_id}/download")
async def download_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Download a document file"""
    
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Check access permissions
    if (current_user.role == "student" and document.uploaded_by != current_user.id) or \
       (current_user.role == "staff" and document.uploaded_by != current_user.id and 
        document.department != current_user.department):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    file_path = Path(document.file_path)
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found on server"
        )
    
    return FileResponse(
        path=str(file_path),
        filename=document.filename,
        media_type='application/octet-stream'
    )

@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: str,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    department: Optional[str] = Form(None),
    course_code: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update document metadata"""
    
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Check if user can update this document
    if document.uploaded_by != current_user.id and current_user.role not in ["admin", "supervisor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own documents"
        )
    
    # Update fields if provided
    if title is not None:
        document.title = title
    if description is not None:
        document.description = description
    if category is not None:
        document.category = category
    if tags is not None:
        document.tags = [tag.strip() for tag in tags.split(',')]
    if department is not None:
        document.department = department
    if course_code is not None:
        document.course_code = course_code
    
    document.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(document)
    
    return DocumentResponse(
        id=document.id,
        title=document.title,
        description=document.description,
        category=document.category,
        tags=document.tags,
        department=document.department,
        course_code=document.course_code,
        filename=document.filename,
        file_size=document.file_size,
        file_type=document.file_type,
        status=document.status,
        uploaded_by=document.uploaded_by,
        reviewed_by=document.reviewed_by,
        created_at=document.created_at,
        updated_at=document.updated_at,
        download_url=f"/api/v1/documents/{document.id}/download"
    )

@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a document"""
    
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Check if user can delete this document
    if document.uploaded_by != current_user.id and current_user.role not in ["admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own documents"
        )
    
    # Delete file from disk
    file_path = Path(document.file_path)
    if file_path.exists():
        file_path.unlink()
    
    # Delete document record
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}

@router.post("/{document_id}/review")
async def review_document(
    document_id: str,
    action: str = Form(...),  # "approve" or "reject"
    comments: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Review a document (approve or reject)"""
    
    if current_user.role not in ["supervisor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only supervisors and admins can review documents"
        )
    
    if action not in ["approve", "reject"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Action must be 'approve' or 'reject'"
        )
    
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Update document status
    document.status = "approved" if action == "approve" else "rejected"
    document.reviewed_by = current_user.id
    document.review_comments = comments
    document.reviewed_at = datetime.utcnow()
    document.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": f"Document {action}d successfully"}
