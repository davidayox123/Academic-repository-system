from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, Query, Request
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, asc, func, and_, or_
from typing import List, Optional, Dict, Any
import os
import uuid
import shutil
import logging
from pathlib import Path
from datetime import datetime
import json
import mimetypes
import aiofiles
import hashlib
from PIL import Image
import fitz  # PyMuPDF for PDF processing

from app.core.database import get_db
from app.models.user import User, UserRole
from app.models.document import Document, DocumentStatus, DocumentCategory, DocumentType
from app.models.department import Department
from app.models.download import Download
from app.schemas.document import DocumentCreate, DocumentResponse, DocumentUpdate, DocumentFilter
from .websocket import notify_document_uploaded
from app.core.auth import get_current_user

router = APIRouter()

# Create uploads directory structure
BASE_DIR = Path(__file__).parent.parent.parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
DOCUMENTS_DIR = UPLOAD_DIR / "documents"
THUMBNAILS_DIR = UPLOAD_DIR / "thumbnails"
PREVIEWS_DIR = UPLOAD_DIR / "previews"

# Create directories
for dir_path in [UPLOAD_DIR, DOCUMENTS_DIR, THUMBNAILS_DIR, PREVIEWS_DIR]:
    dir_path.mkdir(exist_ok=True, parents=True)

# File configuration
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {
    '.pdf', '.doc', '.docx', '.txt', '.md', '.tex', 
    '.ppt', '.pptx', '.xls', '.xlsx', '.csv',
    '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp',
    '.mp4', '.webm', '.mov', '.avi',
    '.mp3', '.wav', '.ogg',
    '.zip', '.rar', '.7z'
}

DOCUMENT_TYPE_MAPPING = {
    '.pdf': DocumentType.PDF,
    '.doc': DocumentType.DOC,
    '.docx': DocumentType.DOCX,
    '.ppt': DocumentType.PPT,
    '.pptx': DocumentType.PPTX,
    '.txt': DocumentType.TXT,
    '.md': DocumentType.TXT,
    '.png': DocumentType.IMAGE,
    '.jpg': DocumentType.IMAGE,
    '.jpeg': DocumentType.IMAGE,
    '.gif': DocumentType.IMAGE,
    '.svg': DocumentType.IMAGE,
    '.webp': DocumentType.IMAGE,
    '.mp4': DocumentType.VIDEO,
    '.webm': DocumentType.VIDEO,
    '.mov': DocumentType.VIDEO,
    '.mp3': DocumentType.AUDIO,
    '.wav': DocumentType.AUDIO,
    '.ogg': DocumentType.AUDIO,
    '.zip': DocumentType.ARCHIVE,
    '.rar': DocumentType.ARCHIVE,
    '.7z': DocumentType.ARCHIVE
}

def validate_file_type(filename: str) -> bool:
    """Validate if file type is allowed"""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

def get_file_size_mb(file_size: int) -> float:
    """Convert file size to MB"""
    return file_size / (1024 * 1024)

def get_document_type(filename: str) -> DocumentType:
    """Get document type based on file extension"""
    ext = Path(filename).suffix.lower()
    return DOCUMENT_TYPE_MAPPING.get(ext, DocumentType.PDF)

async def generate_thumbnail(file_path: Path, document_id: str) -> Optional[str]:
    """Generate thumbnail for supported file types"""
    try:
        thumbnail_path = THUMBNAILS_DIR / f"{document_id}.jpg"
        
        # Handle different file types
        if file_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.webp']:
            # Image thumbnail
            with Image.open(file_path) as img:
                img.thumbnail((300, 300))
                img.save(thumbnail_path, "JPEG")
                return str(thumbnail_path)
                
        elif file_path.suffix.lower() == '.pdf':
            # PDF thumbnail
            doc = fitz.open(file_path)
            if len(doc) > 0:
                page = doc[0]
                mat = fitz.Matrix(1.0, 1.0)
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("ppm")
                
                with Image.open(io.BytesIO(img_data)) as img:
                    img.thumbnail((300, 300))
                    img.save(thumbnail_path, "JPEG")
                    return str(thumbnail_path)
            doc.close()
            
    except Exception as e:
        print(f"Error generating thumbnail: {e}")
        
    return None

async def extract_text_content(file_path: Path) -> Optional[str]:
    """Extract text content for search indexing"""
    try:
        if file_path.suffix.lower() == '.pdf':
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text[:5000]  # Limit to first 5000 chars
            
        elif file_path.suffix.lower() in ['.txt', '.md']:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
                return content[:5000]
                
    except Exception as e:
        print(f"Error extracting text: {e}")
        
    return None

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(""),
    category: str = Form("research"),
    tags: str = Form(""),
    department_id: str = Form(""),
    course_code: str = Form(""),
    is_public: bool = Form(False),
    uploader_id: str = Form(""),  # Add uploader_id parameter
    db: Session = Depends(get_db)
):
    """Upload a new document"""
    try:
        # Basic validation
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file selected")
        
        # Get file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"File type {file_ext} not allowed")
        
        # Read file content
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Empty file")
        
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")
          # Get first department if none provided
        if not department_id:
            first_dept = db.query(Department).first()
            department_id = first_dept.id if first_dept else None
        
        # Use provided uploader_id or fallback to mock user for demo
        if not uploader_id:
            uploader_id = "7e3cf886-559d-43de-b69c-f3772398f03a"  # Default to student user
        
        # Create document record
        document_id = str(uuid.uuid4())
        filename = f"{document_id}{file_ext}"
        file_path = DOCUMENTS_DIR / filename
        
        # Save file asynchronously
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)        # Create database record
        document = Document(
            id=document_id,
            title=title,
            description=description,
            filename=filename,
            original_filename=file.filename,
            file_path=str(file_path),
            file_size=len(content),
            mime_type=file.content_type or "application/octet-stream",
            file_type=file.content_type or "application/octet-stream",
            file_extension=Path(file.filename).suffix.lower(),
            category=DocumentCategory(category),
            document_type=get_document_type(file.filename),
            tags=tags.split(',') if tags else [],
            department_id=department_id,
            course_code=course_code,
            uploader_id=uploader_id,  # Use the actual uploader_id
            is_public=is_public,
            status=DocumentStatus.PENDING
        )
        db.add(document)
        db.commit()
        db.refresh(document)
        
        # Get the uploader and department info for the response
        uploader = db.query(User).filter(User.id == uploader_id).first()
        department = db.query(Department).filter(Department.id == department_id).first()
        
        # Create the response with the correct format
        response_data = {
            "id": document.id,
            "title": document.title,
            "description": document.description,
            "category": document.category.value,
            "tags": document.tags or [],
            "department": department.name if department else "Unknown",
            "course_code": document.course_code,
            "filename": document.original_filename,
            "file_size": document.file_size,
            "file_type": document.file_type,
            "status": document.status.value,
            "uploaded_by": uploader.name if uploader else "Unknown",
            "reviewed_by": None,
            "review_comments": None,
            "reviewed_at": None,
            "created_at": document.created_at,
            "updated_at": document.updated_at,
            "download_url": f"/api/v1/documents/{document.id}/download"
        }
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Upload error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
    # Check file size
    file_size = 0
    content = await file.read()
    file_size = len(content)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE // 1024 // 1024}MB"
        )
    
    if file_size == 0:
        raise HTTPException(status_code=400, detail="Empty file")
    
    try:
        # Generate unique filename
        document_id = str(uuid.uuid4())
        file_extension = Path(file.filename).suffix.lower()
        safe_filename = f"{document_id}{file_extension}"
        file_path = DOCUMENTS_DIR / safe_filename
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        # Process tags
        tag_list = []
        if tags:
            try:
                tag_list = json.loads(tags) if tags.startswith('[') else tags.split(',')
                tag_list = [tag.strip() for tag in tag_list if tag.strip()]
            except:
                tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
          # Create document record
        document = Document(
            id=document_id,
            title=title,
            description=description,
            filename=safe_filename,
            original_filename=file.filename,
            file_path=str(file_path),
            file_size=file_size,
            file_extension=file_extension,
            mime_type=mimetypes.guess_type(file.filename)[0] or "application/octet-stream",
            category=DocumentCategory(category),
            document_type=get_document_type(file.filename),
            tags=tag_list,
            course_code=course_code,
            academic_year=academic_year,
            semester=semester,
            is_public=is_public,            uploader_id=uploader_id or "7e3cf886-559d-43de-b69c-f3772398f03a",  # Use real uploader_id
            department_id=department_id or "7e3cf886-559d-43de-b69c-f3772398f03a",
            status=DocumentStatus.PENDING
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        # Generate thumbnail (async)
        try:
            thumbnail_path = await generate_thumbnail(file_path, document_id)
            if thumbnail_path:
                document.thumbnail_path = thumbnail_path
        except Exception as e:
            print(f"Thumbnail generation failed: {e}")
        
        # Extract text content (async)
        try:
            text_content = await extract_text_content(file_path)
            if text_content:
                document.text_content = text_content
        except Exception as e:
            print(f"Text extraction failed: {e}")
        
        # Update document with processed data
        await db.commit()
        
        # Notify WebSocket clients
        await notify_document_uploaded("mock-user-id", {
            "id": document_id,
            "title": title,
            "category": category,
            "file_size": file_size,
            "timestamp": document.created_at.isoformat()
        })
        
        return DocumentResponse(
            id=document.id,
            title=document.title,
            description=document.description,
            filename=document.filename,
            original_filename=document.original_filename,
            file_size=document.file_size,
            file_type=document.file_type,
            category=document.category.value,
            tags=document.tags or [],
            status=document.status.value,
            upload_date=document.upload_date,
            uploader_name="Mock User",
            department_name="Mock Department",
            download_count=document.download_count,
            view_count=document.view_count
        )
        
    except Exception as e:
        # Clean up file if database operation failed
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

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

@router.get("/", response_model=Dict[str, Any])
async def get_documents(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    department_id: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    sort_by: str = Query("upload_date"),
    sort_order: str = Query("desc"),
    db: Session = Depends(get_db)
):
    """Get documents with filtering and pagination"""
    try:
        # Build query
        query = db.query(Document).options(
            joinedload(Document.uploader),
            joinedload(Document.department)
        )
        
        # Apply filters
        if search:
            search_filter = or_(
                Document.title.ilike(f"%{search}%"),
                Document.description.ilike(f"%{search}%"),
                Document.keywords.ilike(f"%{search}%"),
                Document.text_content.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if category:
            query = query.filter(Document.category == DocumentCategory(category))
        
        if status:
            query = query.filter(Document.status == DocumentStatus(status))
        if department_id:
            query = query.filter(Document.department_id == department_id)
        
        # Apply role-based filtering
        if role and user_id:
            if role == "student":
                # Students see only their own documents
                query = query.filter(Document.uploader_id == user_id)
            elif role == "staff":
                # Staff see their own documents + department documents
                user = db.query(User).filter(User.id == user_id).first()
                if user and user.department_id:
                    query = query.filter(
                        or_(
                            Document.uploader_id == user_id,
                            Document.department_id == user.department_id
                        )
                    )
            elif role == "supervisor":
                # Supervisors see department documents they supervise
                user = db.query(User).filter(User.id == user_id).first()
                if user and user.department_id:
                    query = query.filter(Document.department_id == user.department_id)
            # Admin sees all documents (no additional filter)
        
        # Apply sorting
        sort_column = getattr(Document, sort_by, Document.upload_date)
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * limit
        documents = query.offset(offset).limit(limit).all()
        
        # Format response
        items = []
        for doc in documents:
            items.append({
                "id": doc.id,
                "title": doc.title,
                "description": doc.description,
                "filename": doc.filename,
                "original_filename": doc.original_filename,
                "file_size": doc.file_size,
                "file_type": doc.file_type,
                "category": doc.category.value,
                "document_type": doc.document_type.value if doc.document_type else None,
                "tags": doc.tags or [],
                "status": doc.status.value,
                "is_public": doc.is_public,
                "upload_date": doc.upload_date.isoformat(),
                "uploader_name": doc.uploader.name if doc.uploader else "Unknown",
                "department_name": doc.department.name if doc.department else "Unknown",
                "download_count": doc.download_count,
                "view_count": doc.view_count,
                "thumbnail_path": doc.thumbnail_path
            })
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch documents: {str(e)}")

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific document by ID"""
    document = db.query(Document).options(
        joinedload(Document.uploader),
        joinedload(Document.department)
    ).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Increment view count
    document.view_count = (document.view_count or 0) + 1
    document.last_accessed = datetime.now()
    await db.commit()
    
    return DocumentResponse(
        id=document.id,
        title=document.title,
        description=document.description,
        filename=document.filename,
        original_filename=document.original_filename,
        file_size=document.file_size,
        file_type=document.file_type,
        category=document.category.value,
        tags=document.tags or [],
        status=document.status.value,
        upload_date=document.upload_date,
        uploader_name=document.uploader.name if document.uploader else "Unknown",
        department_name=document.department.name if document.department else "Unknown",
        download_count=document.download_count,
        view_count=document.view_count
    )

@router.get("/{document_id}/download")
async def download_document(
    document_id: str,
    request: Request,
    user_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Download a document file"""
    try:
        document = db.query(Document).filter(Document.id == document_id).first()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        file_path = Path(document.file_path)
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found on server")
        
        # Create download record
        download_record = Download(
            document_id=document_id,
            user_id=user_id or "anonymous",
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            file_size_at_download=document.file_size,
            download_source="web"
        )
        
        db.add(download_record)
        
        # Update download count
        document.download_count = (document.download_count or 0) + 1
        db.commit()
        
        # Return file with proper headers
        return FileResponse(
            path=file_path,
            filename=document.original_filename,
            media_type=document.mime_type or 'application/octet-stream'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Download error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")
    await db.commit()
    
    return FileResponse(
        path=file_path,
        filename=document.original_filename,
        media_type=document.mime_type
    )

@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: str,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    course_code: Optional[str] = Form(None),
    is_public: Optional[bool] = Form(None),
    db: Session = Depends(get_db)
):
    """Update document metadata"""
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Update fields
    if title is not None:
        document.title = title
    if description is not None:
        document.description = description
    if category is not None:
        document.category = DocumentCategory(category)
    if tags is not None:
        try:
            tag_list = json.loads(tags) if tags.startswith('[') else tags.split(',')
            document.tags = [tag.strip() for tag in tag_list if tag.strip()]
        except:
            document.tags = [tag.strip() for tag in tags.split(',') if tag.strip()]
    if course_code is not None:
        document.course_code = course_code
    if is_public is not None:
        document.is_public = is_public
    
    document.updated_at = datetime.now()
    await db.commit()
    
    return DocumentResponse(
        id=document.id,
        title=document.title,
        description=document.description,
        filename=document.filename,
        original_filename=document.original_filename,
        file_size=document.file_size,
        file_type=document.file_type,
        category=document.category.value,
        tags=document.tags or [],
        status=document.status.value,
        upload_date=document.upload_date,
        uploader_name="Mock User",
        department_name="Mock Department",
        download_count=document.download_count,
        view_count=document.view_count
    )

@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """Delete a document"""
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete file from filesystem
    file_path = Path(document.file_path)
    if file_path.exists():
        file_path.unlink()
    
    # Delete thumbnail if exists
    if document.thumbnail_path:
        thumbnail_path = Path(document.thumbnail_path)
        if thumbnail_path.exists():
            thumbnail_path.unlink()
    
    # Delete from database
    db.delete(document)
    await db.commit()
    
    return {"message": "Document deleted successfully"}

@router.post("/{document_id}/review")
async def review_document(
    document_id: str,
    action: str = Form(...),  # "approve" or "reject"
    comments: Optional[str] = Form(None),
    reviewer_id: str = Form(...),  # ID of the reviewing user
    db: Session = Depends(get_db)
):
    """Review a document (approve or reject)"""
    
    # Get reviewer user
    reviewer = db.query(User).filter(User.id == reviewer_id).first()
    if not reviewer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reviewer not found"
        )
    
    if reviewer.role not in ["supervisor", "admin"]:
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
    document.status = DocumentStatus.APPROVED if action == "approve" else DocumentStatus.REJECTED
    document.supervisor_id = reviewer.id  # Use supervisor_id field
    document.reviewer_comments = comments
    document.approval_date = datetime.utcnow() if action == "approve" else None
    document.rejection_reason = comments if action == "reject" else None
    document.updated_at = datetime.utcnow()
    db.commit()
    
    # Send WebSocket notification
    try:
        await notify_document_uploaded({
            "type": "document_reviewed",
            "document_id": document_id,
            "document_title": document.title,
            "action": action,
            "reviewer": reviewer.name,
            "comments": comments
        })
    except Exception as e:
        logging.error(f"Error sending WebSocket notification: {e}")
    
    return {"message": f"Document {action}d successfully"}

@router.get("/stats/overview")
async def get_document_stats(
    db: Session = Depends(get_db)
):
    """Get document statistics"""
    try:
        total_docs = db.query(Document).count()
        pending_docs = db.query(Document).filter(Document.status == DocumentStatus.PENDING).count()
        approved_docs = db.query(Document).filter(Document.status == DocumentStatus.APPROVED).count()
        
        # Category breakdown
        category_stats = db.query(
            Document.category,
            func.count(Document.id).label('count')
        ).group_by(Document.category).all()
        
        # Recent uploads (last 7 days)
        week_ago = datetime.now() - timedelta(days=7)
        recent_uploads = db.query(Document).filter(
            Document.upload_date >= week_ago
        ).count()
        
        # Total file size
        total_size = db.query(func.sum(Document.file_size)).scalar() or 0
        
        return {
            "total_documents": total_docs,
            "pending_reviews": pending_docs,
            "approved_documents": approved_docs,
            "recent_uploads": recent_uploads,
            "total_storage_mb": round(total_size / 1024 / 1024, 2),
            "category_breakdown": [
                {"category": cat.value, "count": count} 
                for cat, count in category_stats
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

# Add missing imports
import io
from datetime import timedelta
