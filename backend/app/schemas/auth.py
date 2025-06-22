from pydantic import BaseModel
from typing import Optional
import uuid
from .user import User

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: User

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
