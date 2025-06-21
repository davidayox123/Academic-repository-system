from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, Query, Request
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, asc, func, and_, or_
from typing import List, Optional, Dict, Any
import os
import uuid
import shutil
from pathlib import Path
from datetime import datetime
import json
import mimetypes
import aiofiles
from PIL import Image
import fitz  # PyMuPDF for PDF processing

from app.core.database import get_db
from app.models.user import User, UserRole
from app.models.document import Document, DocumentStatus, DocumentCategory, DocumentType
from app.models.activity_log import ActivityLog, ActivityType, ActivityLevel
from app.models.download import Download
from app.schemas.document import DocumentCreate, DocumentResponse, DocumentUpdate, DocumentFilter
from .websocket import notify_document_uploaded, notify_activity_update
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

async def log_activity(
    db: Session,
    activity_type: ActivityType,
    title: str,
    description: str,
    user_id: str,
    document_id: Optional[str] = None,
    department_id: Optional[str] = None,
    request: Optional[Request] = None
):
    """Log activity for real-time updates"""
    try:
        ip_address = None
        user_agent = None
        
        if request:
            ip_address = request.client.host if request.client else None
            user_agent = request.headers.get("user-agent")
        
        activity = ActivityLog(
            activity_type=activity_type,
            title=title,
            description=description,
            user_id=user_id,
            document_id=document_id,
            department_id=department_id,
            ip_address=ip_address,
            user_agent=user_agent,
            category="academic",
            is_public='1' if activity_type in [ActivityType.DOCUMENT_UPLOADED, ActivityType.DOCUMENT_APPROVED] else '0'
        )
        
        db.add(activity)
        await db.commit()
        
        # Notify WebSocket clients
        await notify_activity_update({
            "type": activity_type.value,
            "title": title,
            "description": description,
            "timestamp": activity.timestamp.isoformat(),
            "user_id": user_id,
            "document_id": document_id
        })
        
    except Exception as e:
        print(f"Error logging activity: {e}")

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    request: Request,
    file: UploadFile = File(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    category: str = Form(...),
    tags: Optional[str] = Form(None),
    department_id: Optional[str] = Form(None),
    course_code: Optional[str] = Form(None),
    academic_year: Optional[str] = Form(None),
    semester: Optional[str] = Form(None),
    is_public: bool = Form(False),
    db: Session = Depends(get_db)
):
    """Upload a new document"""
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected")
    
    if not validate_file_type(file.filename):
        raise HTTPException(
            status_code=400, 
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
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
            file_type=file.content_type or "application/octet-stream",
            file_extension=file_extension,
            mime_type=mimetypes.guess_type(file.filename)[0] or "application/octet-stream",
            category=DocumentCategory(category),
            document_type=get_document_type(file.filename),
            tags=tag_list,
            course_code=course_code,
            academic_year=academic_year,
            semester=semester,
            is_public=is_public,
            uploader_id="mock-user-id",  # For now, using mock user
            department_id=department_id or "mock-dept-id",
            status=DocumentStatus.PENDING
        )
        
        db.add(document)
        await db.commit()
        await db.refresh(document)
        
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
        
        # Log activity
        await log_activity(
            db=db,
            activity_type=ActivityType.DOCUMENT_UPLOADED,
            title=f"Document uploaded: {title}",
            description=f"New document '{title}' has been uploaded",
            user_id="mock-user-id",
            document_id=document_id,
            department_id=department_id,
            request=request
        )
        
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
    
    # Log view activity
    await log_activity(
        db=db,
        activity_type=ActivityType.DOCUMENT_VIEWED,
        title=f"Document viewed: {document.title}",
        description=f"Document '{document.title}' was viewed",
        user_id="mock-user-id",
        document_id=document_id,
        department_id=document.department_id
    )
    
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
    db: Session = Depends(get_db)
):
    """Download a document file"""
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    file_path = Path(document.file_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found on server")
    
    # Create download record
    download_record = Download(
        document_id=document_id,
        user_id="mock-user-id",
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        file_size_at_download=document.file_size,
        download_source="web"
    )
    
    db.add(download_record)
    
    # Update download count
    document.download_count = (document.download_count or 0) + 1
    await db.commit()
    
    # Log download activity
    await log_activity(
        db=db,
        activity_type=ActivityType.DOCUMENT_DOWNLOADED,
        title=f"Document downloaded: {document.title}",
        description=f"Document '{document.title}' was downloaded",
        user_id="mock-user-id",
        document_id=document_id,
        department_id=document.department_id,
        request=request
    )
    
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
    
    # Log activity
    await log_activity(
        db=db,
        activity_type=ActivityType.DOCUMENT_UPDATED,
        title=f"Document updated: {document.title}",
        description=f"Document '{document.title}' metadata was updated",
        user_id="mock-user-id",
        document_id=document_id,
        department_id=document.department_id
    )
    
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
    
    # Log activity before deletion
    await log_activity(
        db=db,
        activity_type=ActivityType.DOCUMENT_DELETED,
        title=f"Document deleted: {document.title}",
        description=f"Document '{document.title}' was deleted",
        user_id="mock-user-id",
        document_id=document_id,
        department_id=document.department_id
    )
    
    # Delete from database
    db.delete(document)
    await db.commit()
    
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
