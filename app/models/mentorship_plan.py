from sqlalchemy import Column, String, ForeignKey, Numeric, Integer, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel
import uuid

class MentorshipPlan(BaseModel):
    __tablename__ = "mentorship_plans"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    mentorId = Column(UUID(as_uuid=True), ForeignKey('mentor_profiles.id'), nullable=False)
    title = Column(String(200), nullable=False)
    litePrice = Column(Numeric(10, 2), nullable=True)
    standardPrice = Column(Numeric(10, 2), nullable=True)
    proPrice = Column(Numeric(10, 2), nullable=True)
    liteDescription = Column(Text, nullable=True)
    standardDescription = Column(Text, nullable=True)
    proDescription = Column(Text, nullable=True)
    callLimitPerMonth = Column(Integer, nullable=True)
    chatSupport = Column(Boolean, default=False)
    responseTime = Column(String(50), nullable=True)
    handsOnSupport = Column(Boolean, default=False)
    isActive = Column(Boolean, default=True)