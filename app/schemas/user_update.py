from pydantic import BaseModel, Field
from typing import Optional
from pydantic import EmailStr

class UserUpdate(BaseModel):
    """Schema for updating user"""
    email: Optional[EmailStr] = Field(None, description="User's email address")
    username: Optional[str] = Field(None, description="Username")
    password: Optional[str] = Field(None, min_length=8, description="New password (min 8 characters)")