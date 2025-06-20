from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from fastapi.websockets import WebSocketState
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json
import asyncio
import logging

from app.core.database import get_db
from app.core.auth import get_current_user_ws
from app.models.user import User

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_connections: Dict[str, List[str]] = {}

    async def connect(self, websocket: WebSocket, user_id: str, connection_id: str):
        await websocket.accept()
        self.active_connections[connection_id] = websocket
        
        if user_id not in self.user_connections:
            self.user_connections[user_id] = []
        self.user_connections[user_id].append(connection_id)
        
        logging.info(f"WebSocket connected: user_id={user_id}, connection_id={connection_id}")

    def disconnect(self, connection_id: str, user_id: str):
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
        
        if user_id in self.user_connections:
            if connection_id in self.user_connections[user_id]:
                self.user_connections[user_id].remove(connection_id)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
        
        logging.info(f"WebSocket disconnected: user_id={user_id}, connection_id={connection_id}")

    async def send_personal_message(self, message: str, connection_id: str):
        websocket = self.active_connections.get(connection_id)
        if websocket and websocket.client_state == WebSocketState.CONNECTED:
            try:
                await websocket.send_text(message)
            except Exception as e:
                logging.error(f"Error sending message to {connection_id}: {e}")
                await self.remove_connection(connection_id)

    async def send_to_user(self, message: str, user_id: str):
        if user_id in self.user_connections:
            for connection_id in self.user_connections[user_id].copy():
                await self.send_personal_message(message, connection_id)

    async def broadcast(self, message: str):
        disconnected_connections = []
        for connection_id, websocket in self.active_connections.items():
            if websocket.client_state == WebSocketState.CONNECTED:
                try:
                    await websocket.send_text(message)
                except Exception as e:
                    logging.error(f"Error broadcasting to {connection_id}: {e}")
                    disconnected_connections.append(connection_id)
        
        # Clean up disconnected connections
        for connection_id in disconnected_connections:
            await self.remove_connection(connection_id)

    async def remove_connection(self, connection_id: str):
        if connection_id in self.active_connections:
            websocket = self.active_connections[connection_id]
            try:
                await websocket.close()
            except:
                pass
            del self.active_connections[connection_id]
        
        # Remove from user connections
        for user_id, connections in self.user_connections.items():
            if connection_id in connections:
                connections.remove(connection_id)
                if not connections:
                    del self.user_connections[user_id]
                break

manager = ConnectionManager()

@router.websocket("/ws/{connection_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    connection_id: str,
    db: Session = Depends(get_db)
):
    try:
        # Get user from WebSocket (you'll need to implement auth for WebSocket)
        # For now, we'll extract user_id from the connection_id or query params
        # In production, you should implement proper WebSocket authentication
        
        # Accept connection first
        await websocket.accept()
        
        # Try to get user info from query parameters or headers
        query_params = dict(websocket.query_params)
        user_id = query_params.get('user_id')
        
        if not user_id:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": "Authentication required"
            }))
            await websocket.close()
            return
        
        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            await websocket.send_text(json.dumps({
                "type": "error", 
                "message": "Invalid user"
            }))
            await websocket.close()
            return
        
        # Add to connection manager
        manager.active_connections[connection_id] = websocket
        if user_id not in manager.user_connections:
            manager.user_connections[user_id] = []
        manager.user_connections[user_id].append(connection_id)
        
        # Send connection confirmation
        await websocket.send_text(json.dumps({
            "type": "connected",
            "message": "WebSocket connected successfully",
            "user_id": user_id,
            "connection_id": connection_id
        }))
        
        # Keep connection alive and handle messages
        while True:
            try:
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                # Handle different message types
                if message_data.get("type") == "ping":
                    await websocket.send_text(json.dumps({
                        "type": "pong",
                        "timestamp": message_data.get("timestamp")
                    }))
                elif message_data.get("type") == "subscribe":
                    # Handle subscription to specific events
                    await websocket.send_text(json.dumps({
                        "type": "subscribed",
                        "channel": message_data.get("channel", "dashboard")
                    }))
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                logging.error(f"WebSocket error for user {user_id}: {e}")
                break
    
    except Exception as e:
        logging.error(f"WebSocket connection error: {e}")
    
    finally:
        # Clean up connection
        manager.disconnect(connection_id, user_id)

# Utility functions to send real-time updates
async def notify_document_uploaded(user_id: str, document_data: Dict[str, Any]):
    """Notify when a document is uploaded"""
    message = json.dumps({
        "type": "document_uploaded",
        "data": document_data,
        "timestamp": asyncio.get_event_loop().time()
    })
    await manager.send_to_user(message, user_id)

async def notify_document_reviewed(user_id: str, document_data: Dict[str, Any]):
    """Notify when a document is reviewed"""
    message = json.dumps({
        "type": "document_reviewed", 
        "data": document_data,
        "timestamp": asyncio.get_event_loop().time()
    })
    await manager.send_to_user(message, user_id)

async def broadcast_stats_update(stats_data: Dict[str, Any]):
    """Broadcast updated dashboard stats to all connected users"""
    message = json.dumps({
        "type": "stats_update",
        "data": stats_data,
        "timestamp": asyncio.get_event_loop().time()
    })
    await manager.broadcast(message)

async def notify_activity_update(activity_data: Dict[str, Any]):
    """Broadcast new activity to all users"""
    message = json.dumps({
        "type": "activity_update",
        "data": activity_data,
        "timestamp": asyncio.get_event_loop().time()
    })
    await manager.broadcast(message)

# Export the manager for use in other modules
__all__ = ['manager', 'notify_document_uploaded', 'notify_document_reviewed', 
           'broadcast_stats_update', 'notify_activity_update']
