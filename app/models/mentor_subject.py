from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel
import uuid

class MentorSubject(BaseModel):
    __tablename__ = "mentor_subjects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    mentorId = Column(UUID(as_uuid=True), ForeignKey('mentor_profiles.id'), nullable=False)
    subjectId = Column(UUID(as_uuid=True), ForeignKey('subjects.id'), nullable=False)