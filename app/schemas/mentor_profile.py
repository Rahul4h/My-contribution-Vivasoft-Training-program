from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from decimal import Decimal
from ..enums import VerificationStatus

class MentorProfileBase(BaseModel):
    """Base schema for mentor profile"""
    about: Optional[str] = Field(None, description="About the mentor")
    hourly_rate: Optional[Decimal] = Field(None, ge=0, description="Hourly rate in USD")
    is_available: bool = Field(True, description="Whether mentor is available for sessions")
    hiring_card_url: Optional[str] = Field(None, max_length=255, description="URL to mentor's hiring card")

class MentorProfileCreate(MentorProfileBase):
    """Schema for creating mentor profile"""
    user_id: UUID = Field(..., description="ID of the user becoming a mentor")

class MentorProfileUpdate(BaseModel):
    """Schema for updating mentor profile"""
    about: Optional[str] = Field(None, description="About the mentor")
    hourly_rate: Optional[Decimal] = Field(None, ge=0, description="Hourly rate in USD")
    is_available: Optional[bool] = Field(None, description="Whether mentor is available for sessions")
    hiring_card_url: Optional[str] = Field(None, max_length=255, description="URL to mentor's hiring card")

class MentorProfileResponse(MentorProfileBase):
    """Schema for mentor profile response"""
    id: UUID
    user_id: UUID
    verified_status: VerificationStatus
    verification_note: Optional[str]
    total_sessions_conducted: int
    average_rating: Decimal
    review_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True