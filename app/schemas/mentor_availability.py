from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, time
from uuid import UUID
from ..enums import DayOfWeek

class MentorAvailabilityBase(BaseModel):
    """Base schema for mentor availability"""
    day_of_week: DayOfWeek = Field(..., description="Day of the week")
    start_time: time = Field(..., description="Start time of availability")
    end_time: time = Field(..., description="End time of availability")
    timezone: str = Field(..., max_length=50, description="Timezone (e.g., 'UTC', 'America/New_York')")
    is_recurring: bool = Field(True, description="Whether this availability repeats weekly")

class MentorAvailabilityCreate(MentorAvailabilityBase):
    """Schema for creating mentor availability"""
    mentor_id: UUID = Field(..., description="ID of the mentor")

class MentorAvailabilityUpdate(BaseModel):
    """Schema for updating mentor availability"""
    day_of_week: Optional[DayOfWeek] = Field(None, description="Day of the week")
    start_time: Optional[time] = Field(None, description="Start time of availability")
    end_time: Optional[time] = Field(None, description="End time of availability")
    timezone: Optional[str] = Field(None, max_length=50, description="Timezone")
    is_recurring: Optional[bool] = Field(None, description="Whether this availability repeats weekly")

class MentorAvailabilityResponse(MentorAvailabilityBase):
    """Schema for mentor availability response"""
    id: UUID
    mentor_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True