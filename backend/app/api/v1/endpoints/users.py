from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime

from ....core.database import get_db
from ....models.user import User
from ....models.department import Department

router = APIRouter()

@router.get("/", response_model=Dict[str, Any])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    role: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all users with filtering and pagination"""
    
    query = db.query(User).join(Department, User.department_id == Department.id, isouter=True)
    
    # Apply filters
    if role:
        query = query.filter(User.role == role)
    if department:
        query = query.filter(Department.name.contains(department))
    if search:
        query = query.filter(
            (User.name.contains(search)) | 
            (User.email.contains(search))
        )
    
    total = query.count()
    users = query.offset(skip).limit(limit).all()
    
    # Format response
    user_list = []
    for user in users:
        user_list.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.value,
            "department_name": user.department.name if user.department else "Unknown",
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None
        })
    return {
        "items": user_list,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.get("/{user_id}", response_model=dict)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific user by ID"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role.value,
        "department_name": user.department.name if user.department else "Unknown",
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None
    }

@router.get("/stats/overview")
async def get_user_stats(
    db: Session = Depends(get_db)
):
    """Get user statistics overview"""
    
    total_users = db.query(User).count()
    students = db.query(User).filter(User.role == "student").count()
    staff = db.query(User).filter(User.role == "staff").count()
    supervisors = db.query(User).filter(User.role == "supervisor").count()
    admins = db.query(User).filter(User.role == "admin").count()
    
    # Get departments count
    departments_count = db.query(Department).count()
    
    # Get active users
    active_users = db.query(User).filter(User.is_active == True).count()
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "by_role": {
            "students": students,
            "staff": staff,
            "supervisors": supervisors,
            "admins": admins
        },
        "departments_count": departments_count
    }

@router.post("/", response_model=dict)
async def create_user(
    user_data: dict,
    db: Session = Depends(get_db)
):
    """Create a new user"""
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.get("email")).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Get department
    department = None
    if user_data.get("department_id"):
        department = db.query(Department).filter(Department.id == user_data.get("department_id")).first()
        if not department:
            raise HTTPException(status_code=400, detail="Department not found")
    
    user = User(
        name=user_data.get("name"),
        email=user_data.get("email"),
        hashed_password="no_auth_password",  # Since no auth
        role=user_data.get("role", "student"),
        department_id=user_data.get("department_id"),
        is_active=user_data.get("is_active", True)
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role.value,
        "department_name": user.department.name if user.department else "Unknown",
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }

@router.put("/{user_id}", response_model=dict)
async def update_user(
    user_id: str,
    user_data: dict,
    db: Session = Depends(get_db)
):
    """Update a user"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update fields if provided
    if "name" in user_data:
        user.name = user_data["name"]
    if "email" in user_data:
        user.email = user_data["email"]
    if "role" in user_data:
        user.role = user_data["role"]
    if "department_id" in user_data:
        user.department_id = user_data["department_id"]
    if "is_active" in user_data:
        user.is_active = user_data["is_active"]
    
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role.value,
        "department_name": user.department.name if user.department else "Unknown",
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None
    }

@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Delete a user"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}

@router.get("/departments/list")
async def get_departments(
    db: Session = Depends(get_db)
):
    """Get all departments"""
    
    departments = db.query(Department).all()
    return [
        {
            "id": dept.id,
            "name": dept.name,
            "description": dept.description
        }
        for dept in departments
    ]
