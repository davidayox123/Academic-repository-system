from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

from ....core.database import get_db
from ....models import User, Document, ActivityLog, ActivityType

router = APIRouter()

class NotificationCreate(BaseModel):
    user_id: str
    title: str
    message: str
    type: str = "info"
    action_url: Optional[str] = None

class NotificationResponse(BaseModel):
    id: str
    title: str
    message: str
    type: str
    action_url: Optional[str]
    is_read: bool
    created_at: datetime

@router.get("/notifications")
async def get_user_notifications(
    user_id: str = "mock-user-id",
    unread_only: bool = False,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Get user notifications
    """
    try:
        # Mock notifications based on recent activity
        notifications = []
        
        # Get recent activities related to user
        recent_activities = db.query(ActivityLog).filter(
            ActivityLog.created_at >= datetime.now() - timedelta(days=7)
        ).order_by(ActivityLog.created_at.desc()).limit(limit).all()
        
        for activity in recent_activities:
            notification = {
                "id": f"notif_{activity.id}",
                "title": _get_notification_title(activity.activity_type),
                "message": _get_notification_message(activity),
                "type": _get_notification_type(activity.activity_type),
                "action_url": f"/documents/{activity.document_id}" if activity.document_id else None,
                "is_read": False,  # Mock unread status
                "created_at": activity.created_at
            }
            notifications.append(notification)
        
        return {"notifications": notifications}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get notifications: {str(e)}")

@router.post("/notifications/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    db: Session = Depends(get_db)
):
    """
    Mark notification as read
    """
    try:
        # Mock implementation - would update notification status in real system
        return {"message": "Notification marked as read", "notification_id": notification_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to mark notification as read: {str(e)}")

@router.post("/notifications/mark-all-read")
async def mark_all_notifications_read(
    user_id: str = "mock-user-id",
    db: Session = Depends(get_db)
):
    """
    Mark all notifications as read for user
    """
    try:
        # Mock implementation
        return {"message": "All notifications marked as read"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to mark all notifications as read: {str(e)}")

@router.get("/notifications/unread-count")
async def get_unread_count(
    user_id: str = "mock-user-id",
    db: Session = Depends(get_db)
):
    """
    Get count of unread notifications
    """
    try:
        # Mock unread count
        unread_count = 3
        return {"unread_count": unread_count}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get unread count: {str(e)}")

def _get_notification_title(activity_type: ActivityType) -> str:
    """Get notification title based on activity type"""
    titles = {
        ActivityType.DOCUMENT_UPLOADED: "New Document Uploaded",
        ActivityType.DOCUMENT_APPROVED: "Document Approved",
        ActivityType.DOCUMENT_REJECTED: "Document Rejected",
        ActivityType.REVIEW_ASSIGNED: "Review Assigned",
        ActivityType.REVIEW_COMPLETED: "Review Completed",
        ActivityType.DOCUMENT_DOWNLOADED: "Document Downloaded",
        ActivityType.USER_REGISTERED: "New User Registered",
        ActivityType.USER_LOGIN: "User Login",
        ActivityType.SYSTEM_BACKUP: "System Backup"
    }
    return titles.get(activity_type, "System Notification")

def _get_notification_message(activity: ActivityLog) -> str:
    """Get notification message based on activity"""
    if activity.activity_type == ActivityType.DOCUMENT_UPLOADED:
        return f"A new document has been uploaded and is pending review"
    elif activity.activity_type == ActivityType.DOCUMENT_APPROVED:
        return f"Your document has been approved and is now available"
    elif activity.activity_type == ActivityType.DOCUMENT_REJECTED:
        return f"Your document requires revision"
    elif activity.activity_type == ActivityType.REVIEW_ASSIGNED:
        return f"A document has been assigned to you for review"
    elif activity.activity_type == ActivityType.REVIEW_COMPLETED:
        return f"Review has been completed for your document"
    else:
        return f"System activity: {activity.activity_type.value}"

def _get_notification_type(activity_type: ActivityType) -> str:
    """Get notification type for styling"""
    if activity_type in [ActivityType.DOCUMENT_APPROVED]:
        return "success"
    elif activity_type in [ActivityType.DOCUMENT_REJECTED]:
        return "warning"
    elif activity_type in [ActivityType.REVIEW_ASSIGNED]:
        return "info"
    else:
        return "info"

# Background task to send notifications
async def send_notification(notification: NotificationCreate, db: Session):
    """
    Background task to send notification
    """
    # In a real system, this would:
    # 1. Store notification in database
    # 2. Send email/push notification
    # 3. Update real-time UI via WebSocket
    pass
