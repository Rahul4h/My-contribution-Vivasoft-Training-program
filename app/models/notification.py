from sqlalchemy import Column, String, ForeignKey, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from .base_model import BaseModel

class Notification(BaseModel):
    __tablename__ = "notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    notification_type = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)