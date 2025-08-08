from sqlalchemy import Column, String, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel
import uuid

class SessionFeedback(BaseModel):
    __tablename__ = "session_feedback"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    sessionId = Column(UUID(as_uuid=True), ForeignKey('mentorship_sessions.id'), nullable=False)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    feedback = Column(Text, nullable=True)
    rating = Column(Integer, nullable=False)