from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class CategoryBase(BaseModel):
    """Base schema for category"""
    name: str = Field(..., max_length=100, description="Category name")
    description: Optional[str] = Field(None, description="Category description")

class CategoryCreate(CategoryBase):
    """Schema for creating category"""
    pass

class CategoryUpdate(BaseModel):
    """Schema for updating category"""
    name: Optional[str] = Field(None, max_length=100, description="Category name")
    description: Optional[str] = Field(None, description="Category description")

class CategoryResponse(CategoryBase):
    """Schema for category response"""
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True