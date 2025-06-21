from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from ....core.database import get_db
from ....models import (
    User, Document, Department, Review, Download, 
    ActivityLog, DocumentStatus, ActivityType
)

router = APIRouter()

@router.get("/overview")
async def get_analytics_overview(
    role: str = Query("student"),
    department_id: Optional[str] = Query(None),
    timeframe: str = Query("30d"),  # 7d, 30d, 90d, 1y
    db: Session = Depends(get_db)
):
    """
    Get comprehensive analytics overview
    """
    try:
        # Calculate date range
        days = _parse_timeframe(timeframe)
        start_date = datetime.now() - timedelta(days=days)
        
        analytics = {}
        
        if role == "admin":
            analytics = await _get_admin_analytics(db, start_date)
        elif role == "supervisor":
            analytics = await _get_supervisor_analytics(db, start_date, department_id)
        elif role == "staff":
            analytics = await _get_staff_analytics(db, start_date, department_id)
        else:  # student
            analytics = await _get_student_analytics(db, start_date)
        
        return analytics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")

@router.get("/charts/uploads")
async def get_upload_trends(
    role: str = Query("student"),
    department_id: Optional[str] = Query(None),
    timeframe: str = Query("30d"),
    db: Session = Depends(get_db)
):
    """
    Get document upload trends over time
    """
    try:
        days = _parse_timeframe(timeframe)
        start_date = datetime.now() - timedelta(days=days)
        
        # Query uploads by date
        query = db.query(
            func.date(Document.upload_date).label('date'),
            func.count(Document.id).label('count')
        ).filter(Document.upload_date >= start_date)
        
        # Apply role-based filtering
        if role == "supervisor" and department_id:
            query = query.filter(Document.department_id == department_id)
        elif role == "staff" and department_id:
            query = query.filter(Document.department_id == department_id)
        elif role == "student":
            query = query.filter(Document.uploader_id == "mock-user-id")
        
        results = query.group_by(func.date(Document.upload_date)).all()
        
        chart_data = []
        for date, count in results:
            chart_data.append({
                "date": date.isoformat(),
                "uploads": count
            })
        
        return {"chart_data": chart_data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get upload trends: {str(e)}")

@router.get("/charts/categories")
async def get_category_distribution(
    role: str = Query("student"),
    department_id: Optional[str] = Query(None),
    timeframe: str = Query("30d"),
    db: Session = Depends(get_db)
):
    """
    Get document distribution by category
    """
    try:
        days = _parse_timeframe(timeframe)
        start_date = datetime.now() - timedelta(days=days)
        
        query = db.query(
            Document.category,
            func.count(Document.id).label('count')
        ).filter(Document.upload_date >= start_date)
        
        # Apply role-based filtering
        if role == "supervisor" and department_id:
            query = query.filter(Document.department_id == department_id)
        elif role == "staff" and department_id:
            query = query.filter(Document.department_id == department_id)
        elif role == "student":
            query = query.filter(Document.uploader_id == "mock-user-id")
        
        results = query.group_by(Document.category).all()
        
        chart_data = []
        for category, count in results:
            chart_data.append({
                "category": category.value,
                "count": count,
                "percentage": 0  # Will be calculated on frontend
            })
        
        return {"chart_data": chart_data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get category distribution: {str(e)}")

@router.get("/charts/status")
async def get_status_distribution(
    role: str = Query("student"),
    department_id: Optional[str] = Query(None),
    timeframe: str = Query("30d"),
    db: Session = Depends(get_db)
):
    """
    Get document distribution by status
    """
    try:
        days = _parse_timeframe(timeframe)
        start_date = datetime.now() - timedelta(days=days)
        
        query = db.query(
            Document.status,
            func.count(Document.id).label('count')
        ).filter(Document.upload_date >= start_date)
        
        # Apply role-based filtering
        if role == "supervisor" and department_id:
            query = query.filter(Document.department_id == department_id)
        elif role == "staff" and department_id:
            query = query.filter(Document.department_id == department_id)
        elif role == "student":
            query = query.filter(Document.uploader_id == "mock-user-id")
        
        results = query.group_by(Document.status).all()
        
        chart_data = []
        for status, count in results:
            chart_data.append({
                "status": status.value,
                "count": count
            })
        
        return {"chart_data": chart_data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get status distribution: {str(e)}")

@router.get("/performance")
async def get_performance_metrics(
    role: str = Query("student"),
    department_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get system performance metrics
    """
    try:
        metrics = {
            "avg_upload_time": "2.3s",  # Mock data
            "avg_review_time": "48h",
            "approval_rate": 85.7,
            "user_satisfaction": 4.2,
            "storage_efficiency": 92.1,
            "api_response_time": "245ms",
            "uptime": "99.9%",
            "active_users_24h": 127,
            "peak_concurrent_users": 45,
            "bandwidth_usage": "2.4 GB"
        }
        
        return {"metrics": metrics}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get performance metrics: {str(e)}")

# Helper functions

def _parse_timeframe(timeframe: str) -> int:
    """Parse timeframe string to number of days"""
    timeframe_map = {
        "7d": 7,
        "30d": 30,
        "90d": 90,
        "1y": 365
    }
    return timeframe_map.get(timeframe, 30)

async def _get_admin_analytics(db: Session, start_date: datetime) -> Dict[str, Any]:
    """Get analytics for admin role"""
    total_docs = db.query(Document).count()
    total_users = db.query(User).count()
    total_departments = db.query(Department).count()
    
    recent_uploads = db.query(Document).filter(
        Document.upload_date >= start_date
    ).count()
    
    return {
        "overview": {
            "total_documents": total_docs,
            "total_users": total_users,
            "total_departments": total_departments,
            "recent_uploads": recent_uploads,
            "storage_used_gb": 45.2,
            "avg_documents_per_user": round(total_docs / max(total_users, 1), 1)
        },
        "trends": {
            "documents_growth": "+12.5%",
            "users_growth": "+8.3%",
            "activity_growth": "+15.7%"
        }
    }

async def _get_supervisor_analytics(db: Session, start_date: datetime, department_id: str = None) -> Dict[str, Any]:
    """Get analytics for supervisor role"""
    query_filter = []
    if department_id:
        query_filter.append(Document.department_id == department_id)
    
    where_clause = and_(*query_filter) if query_filter else True
    
    pending_reviews = db.query(Document).filter(
        and_(Document.status == DocumentStatus.PENDING, where_clause)
    ).count()
    
    completed_reviews = db.query(Document).filter(
        and_(Document.status.in_([DocumentStatus.APPROVED, DocumentStatus.REJECTED]), where_clause)
    ).count()
    
    return {
        "overview": {
            "pending_reviews": pending_reviews,
            "completed_reviews": completed_reviews,
            "avg_review_time": "48h",
            "approval_rate": 85.7
        },
        "workload": {
            "assigned_this_week": 12,
            "completed_this_week": 8,
            "overdue_reviews": 2
        }
    }

async def _get_staff_analytics(db: Session, start_date: datetime, department_id: str = None) -> Dict[str, Any]:
    """Get analytics for staff role"""
    query_filter = []
    if department_id:
        query_filter.append(Document.department_id == department_id)
    
    where_clause = and_(*query_filter) if query_filter else True
    
    dept_documents = db.query(Document).filter(where_clause).count()
    recent_uploads = db.query(Document).filter(
        and_(Document.upload_date >= start_date, where_clause)
    ).count()
    
    return {
        "overview": {
            "department_documents": dept_documents,
            "recent_uploads": recent_uploads,
            "collaboration_score": 4.2,
            "department_ranking": 3
        },
        "activity": {
            "uploads_this_month": recent_uploads,
            "downloads_received": 234,
            "citations": 45
        }
    }

async def _get_student_analytics(db: Session, start_date: datetime) -> Dict[str, Any]:
    """Get analytics for student role"""
    my_documents = db.query(Document).filter(
        Document.uploader_id == "mock-user-id"
    ).count()
    
    recent_uploads = db.query(Document).filter(
        and_(
            Document.uploader_id == "mock-user-id",
            Document.upload_date >= start_date
        )
    ).count()
    
    return {
        "overview": {
            "my_documents": my_documents,
            "recent_uploads": recent_uploads,
            "total_downloads": 156,
            "total_views": 1245,
            "average_rating": 4.3
        },
        "engagement": {
            "profile_views": 89,
            "document_shares": 23,
            "feedback_received": 12
        }
    }
