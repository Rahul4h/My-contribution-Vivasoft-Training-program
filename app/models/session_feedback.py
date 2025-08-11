from sqlalchemy import Column, String, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from .base_model import BaseModel

class SessionFeedback(BaseModel):
    __tablename__ = "session_feedback"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    mentorship_session_id = Column(UUID(as_uuid=True), ForeignKey('mentorship_sessions.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    feedback = Column(Text, nullable=True)
    rating = Column(Integer, nullable=False)