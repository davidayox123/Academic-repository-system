from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, and_, or_
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from ....core.database import get_db
from ....models import (
    User, Document, DocumentStatus, UserRole, Department, 
    Review, ActivityLog, Download, ActivityType
)

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats(
    role: str = Query("student"),
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
                "pending_reviews": db.query(Document).filter(Document.status == DocumentStatus.PENDING).count(),
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
                
                # Category breakdown
                "category_stats": [
                    {"name": category[0].value, "count": category[1]} 
                    for category in db.query(Document.category, func.count(Document.id)).group_by(Document.category).all()
                ],
                
                # Department breakdown
                "department_stats": [
                    {"name": dept[0], "count": dept[1]} 
                    for dept in db.query(Department.name, func.count(Document.id)).join(Document).group_by(Department.name).all()
                ]
            }
            
        elif role == "supervisor":
            # Supervisor sees department-specific and review statistics
            query_filter = []
            if department_id:
                query_filter.append(Document.department_id == department_id)
            
            where_clause = and_(*query_filter) if query_filter else True
            
            stats = {
                "assigned_reviews": db.query(Review).filter(
                    and_(Review.status == "pending", *query_filter) if query_filter else Review.status == "pending"
                ).count(),
                "completed_reviews": db.query(Review).filter(
                    and_(Review.status == "completed", *query_filter) if query_filter else Review.status == "completed"
                ).count(),
                "pending_documents": db.query(Document).filter(
                    and_(Document.status == DocumentStatus.PENDING, where_clause)
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
                "recent_uploads": db.query(Document).filter(
                    and_(
                        Document.upload_date >= datetime.now() - timedelta(days=30),
                        where_clause
                    )
                ).count(),
                "approved_documents": db.query(Document).filter(
                    and_(Document.status == DocumentStatus.APPROVED, where_clause)
                ).count(),
                "my_uploads": db.query(Document).filter(
                    and_(Document.uploader_id == "mock-user-id", where_clause)
                ).count(),
                "pending_reviews": db.query(Document).filter(
                    and_(Document.status == DocumentStatus.PENDING, where_clause)
                ).count(),
                "total_downloads": db.query(Download).join(Document).filter(where_clause).count()
            }
            
        else:  # student
            # Student sees their own statistics
            stats = {
                "my_documents": db.query(Document).filter(Document.uploader_id == "mock-user-id").count(),
                "pending_reviews": db.query(Document).filter(
                    and_(
                        Document.uploader_id == "mock-user-id",
                        Document.status == DocumentStatus.PENDING
                    )
                ).count(),
                "approved_documents": db.query(Document).filter(
                    and_(
                        Document.uploader_id == "mock-user-id",
                        Document.status == DocumentStatus.APPROVED
                    )
                ).count(),
                "total_downloads": db.query(Download).join(Document).filter(
                    Document.uploader_id == "mock-user-id"
                ).count(),
                "recent_uploads": db.query(Document).filter(
                    and_(
                        Document.uploader_id == "mock-user-id",
                        Document.upload_date >= datetime.now() - timedelta(days=30)
                    )
                ).count(),
                "storage_used_mb": round(
                    (db.query(func.sum(Document.file_size)).filter(
                        Document.uploader_id == "mock-user-id"
                    ).scalar() or 0) / 1024 / 1024, 2
                )
            }
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get dashboard stats: {str(e)}")

@router.get("/recent-documents")
async def get_recent_documents(
    role: str = Query("student"),
    department_id: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get recent documents based on user role
    """
    try:
        query = db.query(Document).options(
            joinedload(Document.uploader),
            joinedload(Document.department)
        )
        
        # Apply role-based filtering
        if role == "admin":
            # Admin sees all documents
            pass
        elif role == "supervisor":
            # Supervisor sees department documents and assigned reviews
            if department_id:
                query = query.filter(Document.department_id == department_id)
        elif role == "staff":
            # Staff sees department documents
            if department_id:
                query = query.filter(Document.department_id == department_id)
        else:  # student
            # Student sees only their documents
            query = query.filter(Document.uploader_id == "mock-user-id")
        
        # Get recent documents
        documents = query.order_by(desc(Document.upload_date)).limit(limit).all()
        
        result = []
        for doc in documents:
            result.append({
                "id": doc.id,
                "title": doc.title,
                "filename": doc.original_filename,
                "category": doc.category.value,
                "status": doc.status.value,
                "upload_date": doc.upload_date.isoformat(),
                "file_size": doc.file_size,
                "uploader_name": doc.uploader.name if doc.uploader else "Unknown",
                "department_name": doc.department.name if doc.department else "Unknown",
                "download_count": doc.download_count or 0,
                "view_count": doc.view_count or 0
            })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recent documents: {str(e)}")

@router.get("/recent-activity")
async def get_recent_activity(
    role: str = Query("student"),
    department_id: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get recent activity feed based on user role
    """
    try:
        query = db.query(ActivityLog).options(
            joinedload(ActivityLog.user),
            joinedload(ActivityLog.document)
        )
        
        # Apply role-based filtering
        if role == "admin":
            # Admin sees all activities
            pass
        elif role == "supervisor":
            # Supervisor sees department activities and review-related activities
            if department_id:
                query = query.filter(
                    or_(
                        ActivityLog.department_id == department_id,
                        ActivityLog.activity_type.in_([
                            ActivityType.REVIEW_ASSIGNED,
                            ActivityType.REVIEW_COMPLETED,
                            ActivityType.DOCUMENT_APPROVED,
                            ActivityType.DOCUMENT_REJECTED
                        ])
                    )
                )
        elif role == "staff":
            # Staff sees department activities
            if department_id:
                query = query.filter(ActivityLog.department_id == department_id)
        else:  # student
            # Student sees their own activities and public activities
            query = query.filter(
                or_(
                    ActivityLog.user_id == "mock-user-id",
                    ActivityLog.is_public == '1'
                )
            )
        
        # Get recent activities
        activities = query.order_by(desc(ActivityLog.timestamp)).limit(limit).all()
        
        result = []
        for activity in activities:
            result.append({
                "id": activity.id,
                "type": activity.activity_type.value,
                "title": activity.title,
                "description": activity.description,
                "timestamp": activity.timestamp.isoformat(),
                "user_name": activity.user.name if activity.user else "System",
                "document_title": activity.document.title if activity.document else None,
                "level": activity.activity_level.value,
                "category": activity.category
            })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recent activity: {str(e)}")

@router.get("/analytics")
async def get_dashboard_analytics(
    role: str = Query("student"),
    department_id: Optional[str] = Query(None),
    period: str = Query("month"),  # week, month, quarter, year
    db: Session = Depends(get_db)
):
    """
    Get analytics data for charts and graphs
    """
    try:
        # Determine date range
        now = datetime.now()
        if period == "week":
            start_date = now - timedelta(days=7)
        elif period == "month":
            start_date = now - timedelta(days=30)
        elif period == "quarter":
            start_date = now - timedelta(days=90)
        else:  # year
            start_date = now - timedelta(days=365)
        
        # Upload trends
        upload_query = db.query(
            func.date(Document.upload_date).label('date'),
            func.count(Document.id).label('count')
        ).filter(Document.upload_date >= start_date)
        
        # Apply role-based filtering
        if role != "admin":
            if role == "student":
                upload_query = upload_query.filter(Document.uploader_id == "mock-user-id")
            elif department_id:
                upload_query = upload_query.filter(Document.department_id == department_id)
        
        upload_trends = upload_query.group_by(func.date(Document.upload_date)).all()
        
        # Download trends
        download_query = db.query(
            func.date(Download.download_date).label('date'),
            func.count(Download.id).label('count')
        ).filter(Download.download_date >= start_date)
        
        if role != "admin":
            if role == "student":
                download_query = download_query.join(Document).filter(Document.uploader_id == "mock-user-id")
            elif department_id:
                download_query = download_query.join(Document).filter(Document.department_id == department_id)
        
        download_trends = download_query.group_by(func.date(Download.download_date)).all()
        
        # Status distribution
        status_query = db.query(
            Document.status,
            func.count(Document.id).label('count')
        )
        
        if role != "admin":
            if role == "student":
                status_query = status_query.filter(Document.uploader_id == "mock-user-id")
            elif department_id:
                status_query = status_query.filter(Document.department_id == department_id)
        
        status_distribution = status_query.group_by(Document.status).all()
        
        return {
            "upload_trends": [
                {"date": trend.date.isoformat(), "count": trend.count}
                for trend in upload_trends
            ],
            "download_trends": [
                {"date": trend.date.isoformat(), "count": trend.count}
                for trend in download_trends
            ],
            "status_distribution": [
                {"status": status.status.value, "count": status.count}
                for status in status_distribution
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")
