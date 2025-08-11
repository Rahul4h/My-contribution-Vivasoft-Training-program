from sqlalchemy import Column, ForeignKey, Integer, Numeric, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from .base_model import BaseModel
from ..enums.review_enums import ReviewStatus

class Review(BaseModel):
    __tablename__ = "reviews"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    mentor_id = Column(UUID(as_uuid=True), ForeignKey('mentor_profiles.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    status = Column(Enum(ReviewStatus), default=ReviewStatus.VISIBLE)