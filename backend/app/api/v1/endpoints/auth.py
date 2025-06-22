from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import (
    authenticate_user, 
    create_access_token, 
    create_refresh_token,
    get_password_hash,
    get_current_user
)
from app.models import User, Department
from app.schemas.user import UserCreate, User
from app.schemas.auth import LoginRequest, TokenResponse, ChangePasswordRequest

router = APIRouter()

@router.post("/register", response_model=User)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    department = db.query(Department).filter(Department.id == user_data.department_id).first()
    if not department:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department not found"
        )
    
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        **user_data.model_dump(exclude={"password"}),
        password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=TokenResponse)
async def login(form_data: LoginRequest, db: Session = Depends(get_db)):
    """Login user and return tokens"""
    user = authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": User.from_orm(user)
    }

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(current_user: User = Depends(get_current_user)):
    """Refresh access token"""
    access_token = create_access_token(data={"sub": str(current_user.id)})
    return {
        "access_token": access_token,
        "refresh_token": "",  # Typically you would handle refresh token rotation
        "token_type": "bearer",
        "user": User.from_orm(current_user)
    }

@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Change user password"""
    if not authenticate_user(db, current_user.email, request.old_password):
        raise HTTPException(status_code=400, detail="Incorrect old password")
    
    current_user.password = get_password_hash(request.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user details"""
    return current_user
