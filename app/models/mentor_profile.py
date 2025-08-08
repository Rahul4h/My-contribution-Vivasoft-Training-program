from sqlalchemy import Column, String, ForeignKey, Enum, Text, Numeric, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel
from ..enums import VerificationStatus
import uuid

class MentorProfile(BaseModel):
    __tablename__ = "mentor_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    verifiedStatus = Column(Enum(VerificationStatus), default=VerificationStatus.PENDING)
    verificationNote = Column(Text, nullable=True)
    about = Column(Text, nullable=True)
    hourlyRate = Column(Numeric(10, 2), nullable=True)
    totalSessionsConducted = Column(Integer, default=0)
    averageRating = Column(Numeric(3, 2), default=0)
    reviewCount = Column(Integer, default=0)
    isAvailable = Column(Boolean, default=True)
    hiringCardUrl = Column(String(255), nullable=True)