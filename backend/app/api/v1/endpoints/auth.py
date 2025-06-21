from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta
import uuid

from app.core.database import get_db
from app.core.auth import (
    authenticate_user, 
    create_access_token, 
    create_refresh_token,
    get_password_hash,
    get_current_user,
    verify_token,
    get_user_by_email,
    is_password_strong,
    generate_user_id
)
from app.models import User, Department
from app.schemas import (
    LoginRequest, 
    TokenResponse, 
    UserCreate, 
    UserResponse,
    ChangePasswordRequest,
    BaseResponse
)

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    
    try:
        print(f"🔄 Registration attempt for: {user_data.email}")
        
        # Check if user already exists
        print("🔍 Checking if user exists...")
        existing_user = get_user_by_email(db, user_data.email)
        if existing_user:
            print("❌ User already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        print("✅ User doesn't exist, proceeding...")
        
        # Validate password strength
        print("🔍 Validating password...")
        is_strong, errors = is_password_strong(user_data.password)
        if not is_strong:
            print(f"❌ Password validation failed: {errors}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "Password does not meet requirements", "errors": errors}
            )
        
        print("✅ Password validation passed")
        
        # Check if department exists
        print(f"🔍 Checking department: {user_data.department_id}")
        
    except Exception as e:
        print(f"❌ Registration error: {e}")
        import traceback
        traceback.print_exc()
        raise
    department = db.query(Department).filter(Department.id == user_data.department_id).first()
    if not department:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department not found"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        id=generate_user_id(),
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_data.role,
        department_id=user_data.department_id
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create tokens
    access_token = create_access_token(data={"sub": db_user.id})
    refresh_token = create_refresh_token(data={"sub": db_user.id})
    
    # Prepare user response
    user_response = UserResponse(
        id=db_user.id,
        name=db_user.name,
        email=db_user.email,
        role=db_user.role,
        department_id=db_user.department_id,
        department_name=department.name,
        avatar=db_user.avatar,
        is_active=db_user.is_active,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user_response
    )

@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login user"""
    
    # Authenticate user
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is deactivated"
        )
    
    # Create tokens
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    # Get department info
    department = db.query(Department).filter(Department.id == user.department_id).first()
    
    # Prepare user response
    user_response = UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        department_id=user.department_id,
        department_name=department.name if department else None,
        avatar=user.avatar,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user_response
    )

@router.post("/refresh", response_model=dict)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(get_current_user)):
    """Refresh access token"""
    
    token = credentials.credentials
    payload = verify_token(token, "refresh")
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    new_access_token = create_access_token(data={"sub": user_id})
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user profile"""
    
    # Get department info
    department = db.query(Department).filter(Department.id == current_user.department_id).first()
    
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        role=current_user.role,
        department_id=current_user.department_id,
        department_name=department.name if department else None,
        avatar=current_user.avatar,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    update_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    
    # Update allowed fields
    if "name" in update_data:
        current_user.name = update_data["name"]
    if "avatar" in update_data:
        current_user.avatar = update_data["avatar"]
    
    db.commit()
    db.refresh(current_user)
    
    # Get department info
    department = db.query(Department).filter(Department.id == current_user.department_id).first()
    
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        role=current_user.role,
        department_id=current_user.department_id,
        department_name=department.name if department else None,
        avatar=current_user.avatar,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )

@router.put("/change-password", response_model=BaseResponse)
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    
    # Verify current password
    from app.core.auth import verify_password
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Validate new password strength
    is_strong, errors = is_password_strong(password_data.new_password)
    if not is_strong:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "New password does not meet requirements", "errors": errors}
        )
    
    # Update password
    current_user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()
    
    return BaseResponse(message="Password changed successfully")

@router.post("/logout", response_model=BaseResponse)
async def logout():
    """Logout user (client-side token removal)"""
    return BaseResponse(message="Logged out successfully")
