from sqlalchemy import Column, ForeignKey, Integer, Numeric, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel
from ..enums import ReviewStatus
import uuid

class Review(BaseModel):
    __tablename__ = "reviews"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    mentorId = Column(UUID(as_uuid=True), ForeignKey('mentor_profiles.id'), nullable=False)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    totalReview = Column(Integer, nullable=True)
    comment = Column(Text, nullable=True)
    reviewStatus = Column(Enum(ReviewStatus), default=ReviewStatus.VISIBLE)