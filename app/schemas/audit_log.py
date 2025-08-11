from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class AuditLogBase(BaseModel):
    """Base schema for audit log"""
    action: str = Field(..., max_length=100, description="Action performed")
    details: Optional[str] = Field(None, description="Additional details about the action")

class AuditLogCreate(AuditLogBase):
    """Schema for creating audit log"""
    user_id: UUID = Field(..., description="ID of the user who performed the action")

class AuditLogResponse(AuditLogBase):
    """Schema for audit log response"""
    id: UUID
    user_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True