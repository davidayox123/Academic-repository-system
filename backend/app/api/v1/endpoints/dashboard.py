from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from typing import List, Dict, Any
from datetime import datetime, timedelta

from ....core.database import get_db
from ....core.auth import get_current_user
from ....models import User, Document, DocumentStatus, UserRole, Department, Review, AuditLog, Download

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get dashboard statistics based on user role and business rules
    """
    stats = {}
    
    if current_user.role == UserRole.ADMIN:
        # Admin sees system-wide statistics
        stats = {
            "total_users": db.query(User).count(),
            "total_documents": db.query(Document).count(),
            "total_departments": db.query(Department).count(),
            "pending_reviews": db.query(Document).filter(Document.status == DocumentStatus.PENDING).count(),
            "approved_documents": db.query(Document).filter(Document.status == DocumentStatus.APPROVED).count(),
            "rejected_documents": db.query(Document).filter(Document.status == DocumentStatus.REJECTED).count(),
            "recent_uploads": db.query(Document).order_by(desc(Document.upload_date)).limit(10).all(),
            "user_breakdown": {
                "students": db.query(User).filter(User.role == UserRole.STUDENT).count(),
                "staff": db.query(User).filter(User.role == UserRole.STAFF).count(),
                "supervisors": db.query(User).filter(User.role == UserRole.SUPERVISOR).count(),
                "admins": db.query(User).filter(User.role == UserRole.ADMIN).count(),
            }
        }
        
    elif current_user.role == UserRole.SUPERVISOR:
        # Supervisor sees department-specific data (business rule)
        dept_documents = db.query(Document).filter(Document.department_id == current_user.assigned_department)
        stats = {
            "department_documents": dept_documents.count(),
            "pending_reviews": dept_documents.filter(Document.status == DocumentStatus.PENDING).count(),
            "approved_by_me": dept_documents.filter(
                and_(Document.supervisor_id == current_user.id, Document.status == DocumentStatus.APPROVED)
            ).count(),
            "rejected_by_me": dept_documents.filter(
                and_(Document.supervisor_id == current_user.id, Document.status == DocumentStatus.REJECTED)
            ).count(),
            "documents_to_review": dept_documents.filter(
                and_(Document.status == DocumentStatus.PENDING, Document.supervisor_id.is_(None))
            ).all(),
            "my_reviews": db.query(Review).filter(Review.user_id == current_user.id).count()
        }
        
    elif current_user.role in [UserRole.STUDENT, UserRole.STAFF]:
        # Students and Staff see their own data (business rule)
        my_documents = db.query(Document).filter(Document.uploader_id == current_user.id)
        stats = {
            "my_documents": my_documents.count(),
            "pending_documents": my_documents.filter(Document.status == DocumentStatus.PENDING).count(),
            "approved_documents": my_documents.filter(Document.status == DocumentStatus.APPROVED).count(),
            "rejected_documents": my_documents.filter(Document.status == DocumentStatus.REJECTED).count(),
            "total_downloads": db.query(func.sum(Document.download_count)).filter(
                Document.uploader_id == current_user.id
            ).scalar() or 0,
            "recent_uploads": my_documents.order_by(desc(Document.upload_date)).limit(5).all()
        }
    
    return {"status": "success", "data": stats}

@router.get("/recent-activity")
async def get_recent_activity(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 20
):
    """
    Get recent activity based on user role and business rules
    """
    if current_user.role == UserRole.ADMIN:
        # Admin sees all system activity
        activities = db.query(AuditLog).order_by(desc(AuditLog.timestamp)).limit(limit).all()
    elif current_user.role == UserRole.SUPERVISOR:
        # Supervisor sees department activity
        activities = db.query(AuditLog).join(Document).filter(
            Document.department_id == current_user.assigned_department
        ).order_by(desc(AuditLog.timestamp)).limit(limit).all()
    else:
        # Students and Staff see their own activity
        activities = db.query(AuditLog).filter(
            AuditLog.user_id == current_user.id
        ).order_by(desc(AuditLog.timestamp)).limit(limit).all()
    
    return {"status": "success", "data": activities}

@router.get("/department-stats")
async def get_department_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get department-wise statistics (Admin and Supervisor access only)
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPERVISOR]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if current_user.role == UserRole.ADMIN:
        # Admin sees all departments
        departments = db.query(Department).all()
    else:
        # Supervisor sees only their assigned department
        departments = db.query(Department).filter(
            Department.id == current_user.assigned_department
        ).all()
    
    dept_stats = []
    for dept in departments:
        dept_data = {
            "department": dept.name,
            "faculty": dept.faculty,
            "total_users": db.query(User).filter(User.department_id == dept.id).count(),
            "total_documents": db.query(Document).filter(Document.department_id == dept.id).count(),
            "pending_documents": db.query(Document).filter(
                and_(Document.department_id == dept.id, Document.status == DocumentStatus.PENDING)
            ).count(),
            "approved_documents": db.query(Document).filter(
                and_(Document.department_id == dept.id, Document.status == DocumentStatus.APPROVED)
            ).count()
        }
        dept_stats.append(dept_data)
    
    return {"status": "success", "data": dept_stats}

@router.get("/upload-trends")
async def get_upload_trends(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    days: int = 30
):
    """
    Get upload trends over time
    """
    start_date = datetime.now() - timedelta(days=days)
    
    if current_user.role == UserRole.ADMIN:
        # Admin sees system-wide trends
        uploads = db.query(
            func.date(Document.upload_date).label('date'),
            func.count(Document.id).label('count')
        ).filter(Document.upload_date >= start_date).group_by(
            func.date(Document.upload_date)
        ).all()
        
    elif current_user.role == UserRole.SUPERVISOR:
        # Supervisor sees department trends
        uploads = db.query(
            func.date(Document.upload_date).label('date'),
            func.count(Document.id).label('count')
        ).filter(
            and_(
                Document.upload_date >= start_date,
                Document.department_id == current_user.assigned_department
            )
        ).group_by(func.date(Document.upload_date)).all()
        
    else:
        # Students and Staff see their own trends
        uploads = db.query(
            func.date(Document.upload_date).label('date'),
            func.count(Document.id).label('count')
        ).filter(
            and_(
                Document.upload_date >= start_date,
                Document.uploader_id == current_user.id
            )
        ).group_by(func.date(Document.upload_date)).all()
    
    trend_data = [{"date": str(upload.date), "uploads": upload.count} for upload in uploads]
    
    return {"status": "success", "data": trend_data}
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
