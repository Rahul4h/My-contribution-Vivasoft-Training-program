from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class UserProfileBase(BaseModel):
    """Base schema for user profile"""
    first_name: Optional[str] = Field(None, max_length=50, description="User's first name")
    last_name: Optional[str] = Field(None, max_length=50, description="User's last name")
    skills: Optional[List[str]] = Field(None, description="List of user's skills")
    education: Optional[List[str]] = Field(None, description="List of user's education")
    about: Optional[str] = Field(None, description="About the user")
    bio: Optional[str] = Field(None, description="User's bio")
    phone: Optional[str] = Field(None, max_length=20, description="User's phone number")
    profile_image: Optional[str] = Field(None, max_length=255, description="URL to profile image")

class UserProfileCreate(UserProfileBase):
    """Schema for creating user profile"""
    user_id: UUID = Field(..., description="ID of the user")

class UserProfileUpdate(UserProfileBase):
    """Schema for updating user profile"""
    pass

class UserProfileResponse(UserProfileBase):
    """Schema for user profile response"""
    id: UUID
    user_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True