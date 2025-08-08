from sqlalchemy import Column, String, ForeignKey, ARRAY, Text
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel
import uuid

class UserProfile(BaseModel):
    __tablename__ = "user_profile"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    firstName = Column(String(50), nullable=True)
    lastName = Column(String(50), nullable=True)
    skills = Column(ARRAY(String), nullable=True)
    education = Column(ARRAY(String), nullable=True)
    about = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)
    phone = Column(String(20), unique=True, nullable=True)
    profileImage = Column(String(255), nullable=True)