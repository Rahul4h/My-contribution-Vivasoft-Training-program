from sqlalchemy import Column, String, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from .base_model import BaseModel
from ..enums.user_enums import UserRole, OAuthProvider

class User(BaseModel):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.STUDENT)
    is_email_verified = Column(Boolean, default=False)
    oauth_provider = Column(Enum(OAuthProvider), nullable=True)
    oauth_id = Column(String(100), nullable=True)
    referred_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    last_login = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Authentication fields
    reset_token = Column(String(255), nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    refresh_token = Column(String(500), nullable=True)
    email_verification_token = Column(String(255), nullable=True)
    email_verification_expires = Column(DateTime, nullable=True)