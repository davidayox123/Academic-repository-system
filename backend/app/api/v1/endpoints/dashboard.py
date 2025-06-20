from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict, Any
from datetime import datetime, timedelta

from ...core.database import get_db
from ...core.auth import get_current_user
from ...models import User, Document, DocumentStatus, UserRole

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics for the current user."""
    
    # Base query filters based on user role
    base_query = db.query(Document)
    
    if current_user.role == UserRole.STUDENT:
        # Students see only their own documents
        base_query = base_query.filter(Document.uploader_id == current_user.id)
    elif current_user.role == UserRole.STAFF:
        # Staff see their own + department documents
        base_query = base_query.filter(
            (Document.uploader_id == current_user.id) | 
            (Document.department_id == current_user.department_id)
        )
    # Supervisors and admins see all documents (no additional filter)
    
    # Get counts by status
    total_documents = base_query.count()
    pending_reviews = base_query.filter(Document.status == DocumentStatus.PENDING).count()
    approved_documents = base_query.filter(Document.status == DocumentStatus.APPROVED).count()
    
    # Get total downloads for user's documents
    user_documents = db.query(Document).filter(Document.uploader_id == current_user.id)
    total_downloads = sum(doc.download_count for doc in user_documents)
    
    # Calculate percentage changes (mock data for now)
    # In a real implementation, you'd compare with previous period
    stats = {
        "total_documents": {
            "value": total_documents,
            "change": "+12%",
            "change_type": "positive"
        },
        "pending_reviews": {
            "value": pending_reviews,
            "change": "-8%",
            "change_type": "negative" if pending_reviews > 0 else "neutral"
        },
        "approved_documents": {
            "value": approved_documents,
            "change": "+15%",
            "change_type": "positive"
        },
        "total_downloads": {
            "value": total_downloads,
            "change": "+23%",
            "change_type": "positive"
        }
    }
    
    return stats

@router.get("/recent-documents")
async def get_recent_documents(
    limit: int = 5,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recent documents for the current user."""
    
    base_query = db.query(Document)
    
    if current_user.role == UserRole.STUDENT:
        base_query = base_query.filter(Document.uploader_id == current_user.id)
    elif current_user.role == UserRole.STAFF:
        base_query = base_query.filter(
            (Document.uploader_id == current_user.id) | 
            (Document.department_id == current_user.department_id)
        )
    
    documents = base_query.order_by(desc(Document.created_at)).limit(limit).all()
    
    return [
        {
            "id": doc.id,
            "title": doc.title,
            "status": doc.status.value,
            "uploaded_at": doc.created_at.isoformat(),
            "downloads": doc.download_count,
            "uploader": {
                "name": doc.uploader.name,
                "email": doc.uploader.email
            }
        }
        for doc in documents
    ]

@router.get("/recent-activity")
async def get_recent_activity(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recent activity for the current user."""
    
    # Get recent documents by the user
    recent_docs = db.query(Document).filter(
        Document.uploader_id == current_user.id
    ).order_by(desc(Document.created_at)).limit(3).all()
    
    # Mock activity data - in a real implementation, you'd have an activity log
    activities = []
    
    for doc in recent_docs:
        activities.append({
            "id": f"upload_{doc.id}",
            "type": "upload",
            "message": f'Uploaded "{doc.title}"',
            "timestamp": doc.created_at.isoformat(),
            "document_id": doc.id
        })
        
        if doc.status == DocumentStatus.APPROVED:
            activities.append({
                "id": f"approve_{doc.id}",
                "type": "approve",
                "message": f'Document "{doc.title}" was approved',
                "timestamp": doc.updated_at.isoformat(),
                "document_id": doc.id
            })
    
    # Sort by timestamp and limit
    activities.sort(key=lambda x: x["timestamp"], reverse=True)
    return activities[:limit]

@router.get("/department-stats")
async def get_department_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get department-wise statistics (for supervisors and admins)."""
    
    if current_user.role not in [UserRole.SUPERVISOR, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Get statistics by department
    dept_stats = db.query(
        Document.department_id,
        func.count(Document.id).label('total_documents'),
        func.sum(Document.download_count).label('total_downloads')
    ).group_by(Document.department_id).all()
    
    return [
        {
            "department_id": stat.department_id,
            "total_documents": stat.total_documents,
            "total_downloads": stat.total_downloads or 0
        }
        for stat in dept_stats
    ]

@router.get("/document-trends")
async def get_document_trends(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get document upload trends over the specified number of days."""
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Get documents uploaded in the date range
    documents = db.query(Document).filter(
        Document.created_at >= start_date,
        Document.created_at <= end_date
    )
    
    if current_user.role == UserRole.STUDENT:
        documents = documents.filter(Document.uploader_id == current_user.id)
    elif current_user.role == UserRole.STAFF:
        documents = documents.filter(
            (Document.uploader_id == current_user.id) | 
            (Document.department_id == current_user.department_id)
        )
    
    # Group by date
    daily_counts = {}
    for i in range(days):
        date = start_date + timedelta(days=i)
        daily_counts[date.strftime('%Y-%m-%d')] = 0
    
    for doc in documents:
        date_str = doc.created_at.strftime('%Y-%m-%d')
        if date_str in daily_counts:
            daily_counts[date_str] += 1
    
    return {
        "labels": list(daily_counts.keys()),
        "data": list(daily_counts.values())
    }
