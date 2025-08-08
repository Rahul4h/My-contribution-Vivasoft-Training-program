from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel
import uuid

class Subject(BaseModel):
    __tablename__ = "subjects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    categoryId = Column(UUID(as_uuid=True), ForeignKey('categories.id'), nullable=False)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)