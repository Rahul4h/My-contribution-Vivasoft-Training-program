from sqlalchemy import Column, String, ForeignKey, Enum, Text, Numeric, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from .base_model import BaseModel
from ..enums.mentor_enums import VerificationStatus

class MentorProfile(BaseModel):
    __tablename__ = "mentor_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    verified_status = Column(Enum(VerificationStatus), default=VerificationStatus.PENDING)
    verification_note = Column(Text, nullable=True)
    about = Column(Text, nullable=True)
    hourly_rate = Column(Numeric(10, 2), nullable=True)
    total_sessions_conducted = Column(Integer, default=0)
    average_rating = Column(Numeric(3, 2), default=0)
    review_count = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)
    hiring_card_url = Column(String(255), nullable=True)