from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from fastapi.websockets import WebSocketState
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import json
import asyncio
import logging
from datetime import datetime
import uuid

from app.core.database import get_db
from app.models.user import User, UserRole
from app.models.document import Document

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_connections: Dict[str, List[str]] = {}
        self.room_connections: Dict[str, List[str]] = {}  # For department/role-based rooms

    async def connect(self, websocket: WebSocket, user_id: str, connection_id: str, room: Optional[str] = None):
        await websocket.accept()
        self.active_connections[connection_id] = websocket
        
        # Track user connections
        if user_id not in self.user_connections:
            self.user_connections[user_id] = []
        self.user_connections[user_id].append(connection_id)
        
        # Track room connections
        if room:
            if room not in self.room_connections:
                self.room_connections[room] = []
            self.room_connections[room].append(connection_id)
        
        logging.info(f"WebSocket connected: user_id={user_id}, connection_id={connection_id}, room={room}")
        
        # Send connection confirmation
        await self.send_personal_message(json.dumps({
            "type": "connection_established",
            "message": "Connected to Academic Repository System",
            "connection_id": connection_id,
            "timestamp": datetime.now().isoformat()
        }), connection_id)

    def disconnect(self, connection_id: str, user_id: str, room: Optional[str] = None):
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
        
        # Remove from user connections
        if user_id in self.user_connections:
            if connection_id in self.user_connections[user_id]:
                self.user_connections[user_id].remove(connection_id)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
        
        # Remove from room connections
        if room and room in self.room_connections:
            if connection_id in self.room_connections[room]:
                self.room_connections[room].remove(connection_id)
            if not self.room_connections[room]:
                del self.room_connections[room]
        
        logging.info(f"WebSocket disconnected: user_id={user_id}, connection_id={connection_id}, room={room}")

    async def send_personal_message(self, message: str, connection_id: str):
        websocket = self.active_connections.get(connection_id)
        if websocket and websocket.client_state == WebSocketState.CONNECTED:
            try:
                await websocket.send_text(message)
                return True
            except Exception as e:
                logging.error(f"Error sending message to {connection_id}: {e}")
                await self.remove_connection(connection_id)
                return False
        return False

    async def send_to_user(self, user_id: str, message: Dict[str, Any]):
        """Send message to all connections of a specific user"""
        if user_id in self.user_connections:
            message_str = json.dumps(message)
            tasks = []
            for connection_id in self.user_connections[user_id]:
                tasks.append(self.send_personal_message(message_str, connection_id))
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

    async def send_to_room(self, room: str, message: Dict[str, Any], exclude_user: Optional[str] = None):
        """Send message to all connections in a room"""
        if room in self.room_connections:
            message_str = json.dumps(message)
            tasks = []
            
            for connection_id in self.room_connections[room]:
                # Skip if excluding specific user
                if exclude_user:
                    user_id = self.get_user_id_by_connection(connection_id)
                    if user_id == exclude_user:
                        continue
                
                tasks.append(self.send_personal_message(message_str, connection_id))
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

    async def broadcast_to_all(self, message: Dict[str, Any], exclude_user: Optional[str] = None):
        """Broadcast message to all connected users"""
        message_str = json.dumps(message)
        tasks = []
        
        for connection_id in self.active_connections:
            if exclude_user:
                user_id = self.get_user_id_by_connection(connection_id)
                if user_id == exclude_user:
                    continue
            
            tasks.append(self.send_personal_message(message_str, connection_id))
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    def get_user_id_by_connection(self, connection_id: str) -> Optional[str]:
        """Get user ID by connection ID"""
        for user_id, connections in self.user_connections.items():
            if connection_id in connections:
                return user_id
        return None

    async def remove_connection(self, connection_id: str):
        """Remove a dead connection"""
        user_id = self.get_user_id_by_connection(connection_id)
        if user_id:
            self.disconnect(connection_id, user_id)

    def get_active_users(self) -> List[str]:
        """Get list of currently active user IDs"""
        return list(self.user_connections.keys())

    def get_room_users(self, room: str) -> List[str]:
        """Get list of users in a specific room"""
        if room not in self.room_connections:
            return []
        
        users = []
        for connection_id in self.room_connections[room]:
            user_id = self.get_user_id_by_connection(connection_id)
            if user_id and user_id not in users:
                users.append(user_id)
        return users

    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        return {
            "total_connections": len(self.active_connections),
            "active_users": len(self.user_connections),
            "active_rooms": len(self.room_connections),
            "rooms": {room: len(connections) for room, connections in self.room_connections.items()}
        }

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
    connection_id: str
):
    """
    WebSocket endpoint that doesn't hold database connections.
    Database connections are created only when needed and immediately closed.
    """
    try:
        # Accept connection first
        await websocket.accept()
        
        # Try to get user info from query parameters
        query_params = dict(websocket.query_params)
        user_id = query_params.get('user_id')
        
        if not user_id:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": "Authentication required"
            }))
            await websocket.close()
            return
        
        # Verify user exists (create DB connection only when needed)
        user = None
        try:
            from app.core.database import SessionLocal
            db = SessionLocal()
            try:
                user = db.query(User).filter(User.id == user_id).first()
            finally:
                db.close()  # Immediately close the DB connection
        except Exception as e:
            logging.error(f"Database error during user verification: {e}")
        
        # Add to connection manager
        manager.active_connections[connection_id] = websocket
        if user_id not in manager.user_connections:
            manager.user_connections[user_id] = []
        manager.user_connections[user_id].append(connection_id)
        
        if not user:
            # For demo purposes, create a temporary user session
            # In production, you should enforce proper authentication
            await websocket.send_text(json.dumps({
                "type": "connected",
                "message": "WebSocket connected (demo mode - user not found in database)",
                "user_id": user_id,
                "connection_id": connection_id,
                "warning": "Demo mode: Please use proper authentication in production"
            }))
        else:
            # Send connection confirmation for valid user
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
