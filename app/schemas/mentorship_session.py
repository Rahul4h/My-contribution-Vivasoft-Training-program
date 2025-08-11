from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from decimal import Decimal
from ..enums import SessionType

class MentorshipSessionBase(BaseModel):
    """Base schema for mentorship session"""
    title: str = Field(..., max_length=200, description="Session title")
    description: Optional[str] = Field(None, description="Session description")
    hourly_rate: Optional[Decimal] = Field(None, ge=0, description="Hourly rate for this session")
    duration_minutes: Optional[int] = Field(None, ge=1, description="Session duration in minutes")
    type: SessionType = Field(..., description="Type of session")
    is_active: bool = Field(True, description="Whether session is active")

class MentorshipSessionCreate(MentorshipSessionBase):
    """Schema for creating mentorship session"""
    mentor_id: UUID = Field(..., description="ID of the mentor")

class MentorshipSessionUpdate(BaseModel):
    """Schema for updating mentorship session"""
    title: Optional[str] = Field(None, max_length=200, description="Session title")
    description: Optional[str] = Field(None, description="Session description")
    hourly_rate: Optional[Decimal] = Field(None, ge=0, description="Hourly rate for this session")
    duration_minutes: Optional[int] = Field(None, ge=1, description="Session duration in minutes")
    type: Optional[SessionType] = Field(None, description="Type of session")
    is_active: Optional[bool] = Field(None, description="Whether session is active")

class MentorshipSessionResponse(MentorshipSessionBase):
    """Schema for mentorship session response"""
    id: UUID
    mentor_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True