from sqlalchemy import Column, String, ForeignKey, Numeric, Integer, Boolean, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from .base_model import BaseModel
from ..enums.session_enums import SessionType

class MentorshipSession(BaseModel):
    __tablename__ = "mentorship_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    mentor_profile_id = Column(UUID(as_uuid=True), ForeignKey('mentor_profiles.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    hourly_rate = Column(Numeric(10, 2), nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    type = Column(Enum(SessionType), nullable=False)
    is_active = Column(Boolean, default=True)