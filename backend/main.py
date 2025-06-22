from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import WebSocket, WebSocketDisconnect
from typing import List
import uvicorn
import os
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1.router import api_router
from app.core.auth import get_current_user
from app.models import User

# Create database tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - Skip table creation since we already have the database
    # Base.metadata.create_all(bind=engine)
    
    # Initialize database with sample data - Skip since we have sample data
    # from app.core.init_db import init_sample_data
    # await init_sample_data()
    
    yield
    # Shutdown
    pass

# Initialize FastAPI app
app = FastAPI(
    title="Academic Repository System API",
    description="A comprehensive API for managing academic research documents",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware - Allow all origins for presentation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Must be False when using "*"
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Mount static files
uploads_dir = Path(__file__).parent.parent / "uploads"
uploads_dir.mkdir(exist_ok=True)  # Create directory if it doesn't exist
app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Academic Repository System API is running"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Academic Repository System API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Test CORS endpoint
@app.get("/test-cors")
async def test_cors():
    return {"message": "CORS is working!", "timestamp": "2025-06-21"}

# Simple test endpoint to verify routing
@app.post("/test-register")
async def test_register():
    return {"message": "Test register endpoint reached!"}

# WebSocket connection manager for dashboard updates
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        to_remove = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                to_remove.append(connection)
        for conn in to_remove:
            self.disconnect(conn)

manager = ConnectionManager()

@app.websocket("/ws/dashboard")
async def websocket_dashboard(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive; optionally handle pings/pongs
            await asyncio.sleep(30)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# To broadcast an update from any endpoint, use:
# await manager.broadcast({"type": "dashboard_update", "payload": ...})
# For example, after a document upload or review action.

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
