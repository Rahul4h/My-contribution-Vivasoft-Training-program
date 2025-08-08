from sqlalchemy import Column, String, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel
from ..enums import UserRole, OAuthProvider
import uuid
from datetime import datetime

class User(BaseModel):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashedPassword = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    isEmailVerified = Column(Boolean, default=False)
    oauthProvider = Column(Enum(OAuthProvider), nullable=True)
    oauthId = Column(String(100), nullable=True)
    referredBy = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    lastLogin = Column(DateTime, nullable=True)
    isActive = Column(Boolean, default=True)