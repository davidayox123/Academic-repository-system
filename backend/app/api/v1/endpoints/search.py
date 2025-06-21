from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_, and_
from typing import List, Dict, Any, Optional
from datetime import datetime

from ....core.database import get_db
from ....models import Document, User, Department, DocumentStatus
from ....schemas import DocumentResponse

router = APIRouter()

@router.get("/documents")
async def search_documents(
    q: str = Query(..., description="Search query"),
    role: str = Query("student"),
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    department_id: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Advanced document search with full-text search capabilities
    """
    try:
        query = db.query(Document).options(
            joinedload(Document.uploader),
            joinedload(Document.department)
        )
        
        # Full-text search on title, description, filename
        search_filter = or_(
            Document.title.ilike(f"%{q}%"),
            Document.description.ilike(f"%{q}%"),
            Document.original_filename.ilike(f"%{q}%"),
            Document.extracted_text.ilike(f"%{q}%")
        )
        query = query.filter(search_filter)
        
        # Apply filters
        if category:
            query = query.filter(Document.category == category)
        if status:
            query = query.filter(Document.status == status)
        if department_id:
            query = query.filter(Document.department_id == department_id)
        
        # Apply role-based filtering
        if role == "admin":
            pass  # Admin sees all
        elif role == "supervisor":
            if department_id:
                query = query.filter(Document.department_id == department_id)
        elif role == "staff":
            if department_id:
                query = query.filter(Document.department_id == department_id)
        else:  # student
            query = query.filter(Document.uploader_id == "mock-user-id")
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        documents = query.order_by(Document.upload_date.desc()).offset(offset).limit(limit).all()
        
        results = []
        for doc in documents:
            results.append({
                "id": doc.id,
                "title": doc.title,
                "description": doc.description,
                "filename": doc.original_filename,
                "category": doc.category.value,
                "status": doc.status.value,
                "upload_date": doc.upload_date.isoformat(),
                "file_size": doc.file_size,
                "uploader_name": doc.uploader.name if doc.uploader else "Unknown",
                "department_name": doc.department.name if doc.department else "Unknown",
                "download_count": doc.download_count or 0,
                "view_count": doc.view_count or 0,
                "relevance_score": 1.0  # Mock relevance score
            })
        
        return {
            "items": results,
            "total": total,
            "page": (offset // limit) + 1,
            "limit": limit,
            "total_pages": (total + limit - 1) // limit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.get("/suggestions")
async def get_search_suggestions(
    q: str = Query(..., min_length=2),
    limit: int = Query(5, ge=1, le=10),
    db: Session = Depends(get_db)
):
    """
    Get search suggestions based on partial query
    """
    try:
        # Search in document titles and categories
        title_suggestions = db.query(Document.title).filter(
            Document.title.ilike(f"%{q}%")
        ).limit(limit//2).all()
        
        category_suggestions = db.query(Document.category).filter(
            Document.category.ilike(f"%{q}%")
        ).distinct().limit(limit//2).all()
        
        suggestions = [title[0] for title in title_suggestions]
        suggestions.extend([cat[0] for cat in category_suggestions])
        
        return {"suggestions": suggestions[:limit]}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get suggestions: {str(e)}")

@router.get("/popular")
async def get_popular_searches(
    limit: int = Query(10, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """
    Get popular search terms based on document views/downloads
    """
    try:
        # Get most downloaded/viewed documents and extract keywords
        popular_docs = db.query(Document).order_by(
            (Document.download_count + Document.view_count).desc()
        ).limit(limit).all()
        
        popular_terms = []
        for doc in popular_docs:
            # Extract keywords from title
            words = doc.title.lower().split()
            for word in words:
                if len(word) > 3 and word not in ['and', 'the', 'for', 'with', 'from']:
                    popular_terms.append(word.capitalize())
        
        # Remove duplicates and limit
        unique_terms = list(dict.fromkeys(popular_terms))[:limit]
        
        return {"popular_searches": unique_terms}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get popular searches: {str(e)}")
