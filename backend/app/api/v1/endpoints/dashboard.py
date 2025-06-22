from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, and_, or_
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from ....core.database import get_db
from ....models import (
    User, Document, DocumentStatus, UserRole, Department, 
    Review, Download
)

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats(
    role: str = Query("student"),
    user_id: Optional[str] = Query(None),
    department_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get dashboard statistics based on user role
    """
    try:
        stats = {}
        
        if role == "admin":
            # Admin sees system-wide statistics
            stats = {
                "total_users": db.query(User).count(),
                "total_documents": db.query(Document).count(),
                "total_departments": db.query(Department).count(),
                "pending_reviews": db.query(Document).filter(Document.status == DocumentStatus.SUBMITTED).count(),
                "approved_documents": db.query(Document).filter(Document.status == DocumentStatus.APPROVED).count(),
                "rejected_documents": db.query(Document).filter(Document.status == DocumentStatus.REJECTED).count(),
                "under_review": db.query(Document).filter(Document.status == DocumentStatus.UNDER_REVIEW).count(),
                "total_downloads": db.query(Download).count(),
                "storage_used_mb": round((db.query(func.sum(Document.file_size)).scalar() or 0) / 1024 / 1024, 2),
                
                # Recent activity counts
                "recent_uploads": db.query(Document).filter(
                    Document.upload_date >= datetime.now() - timedelta(days=7)
                ).count(),
                "active_users": db.query(User).filter(User.is_active == True).count(),
                
                # Department breakdown
                "department_stats": [
                    {"name": dept[0], "count": dept[1]} 
                    for dept in db.query(Department.department_name, func.count(Document.id)).join(Document, Document.department_id == Department.department_id).group_by(Department.department_name).all()
                ]
            }
            
        elif role == "supervisor":
            # Supervisor sees department-specific and review statistics
            query_filter = []
            if department_id:
                query_filter.append(Document.department_id == department_id)
            
            where_clause = and_(*query_filter) if query_filter else True
            
            stats = {
                "assigned_reviews": db.query(Document).filter(
                    and_(Document.status == DocumentStatus.SUBMITTED, Document.supervisor_id == user_id)
                ).count(),
                "completed_reviews": db.query(Review).filter(Review.user_id == user_id).count(),
                "pending_documents": db.query(Document).filter(
                    and_(Document.status == DocumentStatus.SUBMITTED, where_clause)
                ).count(),
                "approved_documents": db.query(Document).filter(
                    and_(Document.status == DocumentStatus.APPROVED, where_clause)
                ).count(),
                "department_documents": db.query(Document).filter(where_clause).count(),
                "recent_submissions": db.query(Document).filter(
                    and_(
                        Document.upload_date >= datetime.now() - timedelta(days=7),
                        where_clause
                    )
                ).count(),
                "avg_review_time": 2.5,  # Mock data for now
                "review_workload": "Normal"  # Mock data
            }
            
        elif role == "staff":
            # Staff sees department-specific statistics
            query_filter = []
            if department_id:
                query_filter.append(Document.department_id == department_id)
            
            where_clause = and_(*query_filter) if query_filter else True
            
            stats = {
                "department_documents": db.query(Document).filter(where_clause).count(),
                "approved_documents": db.query(Document).filter(
                    and_(Document.status == DocumentStatus.APPROVED, where_clause)
                ).count(),
                "pending_documents": db.query(Document).filter(
                    and_(Document.status == DocumentStatus.SUBMITTED, where_clause)
                ).count(),
                "rejected_documents": db.query(Document).filter(
                    and_(Document.status == DocumentStatus.REJECTED, where_clause)
                ).count(),
                "your_uploads": db.query(Document).filter(
                    and_(Document.uploader_id == user_id, where_clause)
                ).count(),
                "recent_department_uploads": db.query(Document).filter(
                    and_(
                        Document.upload_date >= datetime.now() - timedelta(days=7),
                        where_clause
                    )
                ).count(),
                "total_department_users": db.query(User).filter(User.department_id == department_id).count(),
                "storage_used_department_mb": round((db.query(func.sum(Document.file_size)).filter(where_clause).scalar() or 0) / 1024 / 1024, 2)
            }
            
        elif role == "student":
            # Student sees their own statistics
            stats = {
                "total_uploads": db.query(Document).filter(Document.uploader_id == user_id).count(),
                "approved_uploads": db.query(Document).filter(
                    and_(Document.uploader_id == user_id, Document.status == DocumentStatus.APPROVED)
                ).count(),
                "rejected_uploads": db.query(Document).filter(
                    and_(Document.uploader_id == user_id, Document.status == DocumentStatus.REJECTED)
                ).count(),
                "pending_reviews": db.query(Document).filter(
                    and_(Document.uploader_id == user_id, Document.status == DocumentStatus.SUBMITTED)
                ).count(),
                "under_review": db.query(Document).filter(
                    and_(Document.uploader_id == user_id, Document.status == DocumentStatus.UNDER_REVIEW)
                ).count(),
                "total_downloads": db.query(Download).join(Document).filter(Document.uploader_id == user_id).count(),
                "average_rating": 4.5,  # Mock data
            }
            
        return stats
        
    except Exception as e:
        print(f"Error fetching dashboard stats: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/recent-documents")
async def get_recent_documents(
    role: str = Query("student"),
    user_id: Optional[str] = Query(None),
    department_id: Optional[str] = Query(None),
    limit: int = Query(5, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get recent documents based on user role
    """
    try:
        query = db.query(
            Document.title,
            Document.status,
            Document.upload_date,
            User.first_name,
            User.last_name
        ).join(User, Document.uploader_id == User.id)

        if role == "admin":
            # Admin sees all recent documents
            query = query.order_by(desc(Document.upload_date))
        
        elif role == "supervisor":
            # Supervisor sees recent documents in their department or assigned for review
            query = query.filter(
                or_(
                    Document.department_id == department_id,
                    Document.supervisor_id == user_id
                )
            ).order_by(desc(Document.upload_date))
            
        elif role == "staff":
            # Staff sees recent documents in their department
            query = query.filter(Document.department_id == department_id).order_by(desc(Document.upload_date))
            
        elif role == "student":
            # Student sees their own recent documents
            query = query.filter(Document.uploader_id == user_id).order_by(desc(Document.upload_date))
            
        else:
            return []

        recent_docs = query.limit(limit).all()
        
        return [
            {
                "title": doc.title,
                "status": doc.status.value,
                "upload_date": doc.upload_date.isoformat(),
                "uploader": f"{doc.first_name} {doc.last_name}"
            }
            for doc in recent_docs
        ]
    except Exception as e:
        print(f"Error fetching recent documents: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/user-profile")
async def get_user_profile_summary(
    user_id: str = Query(...),
    db: Session = Depends(get_db)
):
    """
    Get a summary of the user's profile for the dashboard header
    """
    try:
        user = db.query(
            User.first_name,
            User.last_name,
            User.email,
            User.role,
            Department.department_name
        ).join(Department).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "name": f"{user.first_name} {user.last_name}",
            "email": user.email,
            "role": user.role.value,
            "department": user.department_name
        }
    except Exception as e:
        print(f"Error fetching user profile summary: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/recent-activity")
async def get_recent_activity(
    role: str = Query("student"),
    user_id: Optional[str] = Query(None),
    department_id: Optional[str] = Query(None),
    limit: int = Query(5, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get recent activity for the dashboard (stub implementation).
    """
    # TODO: Implement real activity logs if needed
    return []
