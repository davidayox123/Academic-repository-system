from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, Request, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, asc, func, and_, or_
from typing import List, Optional
import os
import uuid
import shutil
from pathlib import Path

from app.core.database import get_db
from app.models import User, Document, Department, Download, DocumentStatus
from app.schemas.document import DocumentCreate, DocumentResponse, DocumentUpdate, DocumentFilter, DocumentListResponse, UploaderInfo
from .websocket import notify_document_uploaded
from app.core.auth import get_current_user

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
DOCUMENTS_DIR = UPLOAD_DIR / "documents"

DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt'}

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    uploader_id: str = Form(...),
    department_id: str = Form(...),
    supervisor_id: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    request: Request = None
):
    """Upload a new document."""
    if not file.filename or Path(file.filename).suffix.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type.")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds the 50MB limit.")

    document_id = str(uuid.uuid4())
    file_ext = Path(file.filename).suffix
    filename = f"{document_id}{file_ext}"
    file_path = DOCUMENTS_DIR / filename

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    db_document = Document(
        id=document_id,
        title=title,
        uploader_id=uploader_id,
        department_id=department_id,
        supervisor_id=supervisor_id,
        file_path=str(file_path),
        file_size=len(content)
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    # Eager load uploader for the response
    db.refresh(db_document, attribute_names=['uploader'])

    download_url = request.url_for("download_document_file", document_id=db_document.id)

    return DocumentResponse(
        **db_document.__dict__,
        uploader=UploaderInfo(**db_document.uploader.__dict__),
        download_url=str(download_url)
    )

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    db: Session = Depends(get_db),
    request: Request = None
):
    """Retrieve a single document by its ID."""
    doc = db.query(Document).options(joinedload(Document.uploader)).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    download_url = request.url_for("download_document_file", document_id=doc.id)
    
    return DocumentResponse(
        **doc.__dict__,
        uploader=UploaderInfo(**doc.uploader.__dict__),
        download_url=str(download_url)
    )

@router.get("", response_model=DocumentListResponse)
async def get_documents(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    filters: DocumentFilter = Depends(),
    db: Session = Depends(get_db),
    request: Request = None
):
    """Retrieve a paginated list of documents with filtering and sorting."""
    query = db.query(Document).options(joinedload(Document.uploader))

    # Remove or comment out this block if filters.search is not supported
    # if filters.search:
    #     query = query.filter(Document.title.ilike(f"%{filters.search}%"))
    if filters.status:
        query = query.filter(Document.status == filters.status)
    if filters.department_id:
        query = query.filter(Document.department_id == filters.department_id)
    if filters.uploader_id:
        query = query.filter(Document.uploader_id == filters.uploader_id)
    if filters.supervisor_id:
        query = query.filter(Document.supervisor_id == filters.supervisor_id)

    total = query.count()
    
    sort_column = getattr(Document, filters.sort_by, Document.upload_date)
    order = desc if filters.sort_order == "desc" else asc
    query = query.order_by(order(sort_column)).limit(per_page).offset((page - 1) * per_page)

    documents = query.all()

    doc_responses = [
        DocumentResponse(
            **doc.__dict__,
            uploader=UploaderInfo(**doc.uploader.__dict__),
            download_url=str(request.url_for("download_document_file", document_id=doc.id))
        )
        for doc in documents
    ]

    return DocumentListResponse(
        documents=doc_responses,
        total=total,
        page=page,
        pages=(total + per_page - 1) // per_page,
        per_page=per_page
    )

@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: str,
    update_data: DocumentUpdate,
    db: Session = Depends(get_db),
    request: Request = None
):
    """Update a document's details."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(doc, key, value)

    db.commit()
    db.refresh(doc)
    db.refresh(doc, attribute_names=['uploader'])

    download_url = request.url_for("download_document_file", document_id=doc.id)

    return DocumentResponse(
        **doc.__dict__,
        uploader=UploaderInfo(**doc.uploader.__dict__),
        download_url=str(download_url)
    )

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(document_id: str, db: Session = Depends(get_db)):
    """Delete a document."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if os.path.exists(doc.file_path):
        os.remove(doc.file_path)

    db.delete(doc)
    db.commit()
    return

@router.get("/{document_id}/download", response_class=FileResponse)
async def download_document_file(
    document_id: str,
    user_id: str = Query(...),
    db: Session = Depends(get_db)
):
    """Download the physical file for a document and log the action."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc or not doc.file_path or not os.path.exists(doc.file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Log the download action
    new_download = Download(document_id=document_id, user_id=user_id)
    db.add(new_download)
    db.commit()

    return FileResponse(path=doc.file_path, filename=Path(doc.file_path).name, media_type='application/octet-stream')
