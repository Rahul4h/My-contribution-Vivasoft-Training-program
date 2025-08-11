from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from .base_model import BaseModel

class MentorSubject(BaseModel):
    __tablename__ = "mentor_subjects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    mentor_profile_id = Column(UUID(as_uuid=True), ForeignKey('mentor_profiles.id'), nullable=False)
    subject_id = Column(UUID(as_uuid=True), ForeignKey('subjects.id'), nullable=False)