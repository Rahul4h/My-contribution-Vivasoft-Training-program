from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class SubjectBase(BaseModel):
    """Base schema for subject"""
    name: str = Field(..., max_length=100, description="Subject name")
    description: Optional[str] = Field(None, description="Subject description")

class SubjectCreate(SubjectBase):
    """Schema for creating subject"""
    category_id: UUID = Field(..., description="ID of the category this subject belongs to")

class SubjectUpdate(BaseModel):
    """Schema for updating subject"""
    name: Optional[str] = Field(None, max_length=100, description="Subject name")
    description: Optional[str] = Field(None, description="Subject description")
    category_id: Optional[UUID] = Field(None, description="ID of the category this subject belongs to")

class SubjectResponse(SubjectBase):
    """Schema for subject response"""
    id: UUID
    category_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True