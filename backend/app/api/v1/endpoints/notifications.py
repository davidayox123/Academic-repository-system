from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

from ....core.database import get_db
from ....models import User, Document

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
        
        # Get recent documents related to user
        recent_documents = db.query(Document).filter(
            Document.user_id == user_id,
            Document.created_at >= datetime.now() - timedelta(days=7)
        ).order_by(Document.created_at.desc()).limit(limit).all()
        
        for document in recent_documents:
            notification = {
                "id": f"notif_{document.id}",
                "title": "Document Activity",
                "message": f"Document '{document.title}' was recently updated.",
                "type": "info",
                "action_url": f"/documents/{document.id}",
                "is_read": False,  # Mock unread status
                "created_at": document.created_at
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
