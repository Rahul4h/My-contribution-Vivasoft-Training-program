from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from ..enums import ReviewStatus

class ReviewBase(BaseModel):
    """Base schema for review"""
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5 stars")
    total_review: Optional[int] = Field(None, description="Total review score")
    comment: Optional[str] = Field(None, description="Review comment")

class ReviewCreate(ReviewBase):
    """Schema for creating review"""
    mentor_id: UUID = Field(..., description="ID of the mentor being reviewed")
    user_id: UUID = Field(..., description="ID of the user writing the review")

class ReviewUpdate(BaseModel):
    """Schema for updating review"""
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating from 1 to 5 stars")
    total_review: Optional[int] = Field(None, description="Total review score")
    comment: Optional[str] = Field(None, description="Review comment")
    status: Optional[ReviewStatus] = Field(None, description="Review visibility status")

class ReviewResponse(ReviewBase):
    """Schema for review response"""
    id: UUID
    mentor_id: UUID
    user_id: UUID
    status: ReviewStatus
    created_at: datetime
    
    class Config:
        from_attributes = True