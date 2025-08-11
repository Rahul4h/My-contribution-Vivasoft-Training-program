from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class NotificationBase(BaseModel):
    """Base schema for notification"""
    notification_type: str = Field(..., max_length=50, description="Type of notification")
    message: str = Field(..., description="Notification message")

class NotificationCreate(NotificationBase):
    """Schema for creating notification"""
    user_id: UUID = Field(..., description="ID of the user to notify")

class NotificationUpdate(BaseModel):
    """Schema for updating notification"""
    is_read: bool = Field(..., description="Mark notification as read/unread")

class NotificationResponse(NotificationBase):
    """Schema for notification response"""
    id: UUID
    user_id: UUID
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True