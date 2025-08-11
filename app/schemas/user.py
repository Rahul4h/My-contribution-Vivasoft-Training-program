from pydantic import BaseModel, Field, field_serializer
from typing import Optional
from datetime import datetime
import uuid
from uuid import UUID

from pydantic import EmailStr

class UserBase(BaseModel):
    """
    User Base Schema - Base fields for user data
    """
    email: EmailStr
    username: str

class UserCreate(UserBase):
    """
    User Create Schema - Data required to create a new user
    """
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    """
    User Login Schema - Data required for user login
    """
    email: EmailStr
    password: str

class UserResponse(UserBase):
    """
    User Response Schema - Data returned about a user
    """
    id: UUID
    is_active: bool
    created_at: datetime
    
    @field_serializer('id')
    def serialize_id(self, value):
        # Serialize UUID to string for JSON compatibility in API responses
        return str(value)
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    """
    Token Schema - Authentication token data
    """
    access_token: str
    refresh_token: str
    token_type: str
    user_id: str
    email: str

class TokenData(BaseModel):
    """
    Token Data Schema - Data encoded in the token
    """
    email: Optional[str] = None

class PasswordReset(BaseModel):
    """
    Password Reset Schema - Data for password reset
    """
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    """
    Password Reset Confirm Schema - Data to confirm password reset
    """
    token: str
    new_password: str = Field(..., min_length=8)

class RefreshToken(BaseModel):
    """
    Refresh Token Schema - Data for token refresh
    """
    refresh_token: str