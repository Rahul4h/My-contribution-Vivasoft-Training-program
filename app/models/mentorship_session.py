from sqlalchemy import Column, String, ForeignKey, Numeric, Integer, Boolean, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel
from ..enums import SessionType
import uuid

class MentorshipSession(BaseModel):
    __tablename__ = "mentorship_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    mentorId = Column(UUID(as_uuid=True), ForeignKey('mentor_profiles.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    hourlyRate = Column(Numeric(10, 2), nullable=True)
    durationMinutes = Column(Integer, nullable=True)
    sessionType = Column(Enum(SessionType), nullable=False)
    isActive = Column(Boolean, default=True)