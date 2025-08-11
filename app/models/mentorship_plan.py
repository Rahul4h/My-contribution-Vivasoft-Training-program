from sqlalchemy import Column, String, ForeignKey, Numeric, Integer, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from .base_model import BaseModel

class MentorshipPlan(BaseModel):
    __tablename__ = "mentorship_plans"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    mentor_profile_id = Column(UUID(as_uuid=True), ForeignKey('mentor_profiles.id'), nullable=False)
    title = Column(String(200), nullable=False)
    lite_price = Column(Numeric(10, 2), nullable=True)
    standard_price = Column(Numeric(10, 2), nullable=True)
    pro_price = Column(Numeric(10, 2), nullable=True)
    lite_description = Column(Text, nullable=True)
    standard_description = Column(Text, nullable=True)
    pro_description = Column(Text, nullable=True)
    call_limit_per_month = Column(Integer, nullable=True)
    chat_support = Column(Boolean, default=False)
    response_time = Column(String(50), nullable=True)
    hands_on_support = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)