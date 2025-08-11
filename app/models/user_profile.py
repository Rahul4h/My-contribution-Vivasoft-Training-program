from sqlalchemy import Column, String, ForeignKey, ARRAY, Text
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from .base_model import BaseModel

class UserProfile(BaseModel):
    __tablename__ = "user_profile"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    skills = Column(ARRAY(String), nullable=True)
    education = Column(ARRAY(String), nullable=True)
    about = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)
    phone = Column(String(20), unique=True, nullable=True)
    profile_image = Column(String(255), nullable=True)