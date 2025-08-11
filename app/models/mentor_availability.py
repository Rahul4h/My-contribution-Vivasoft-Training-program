from sqlalchemy import Column, String, ForeignKey, Enum, Time, Boolean
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from .base_model import BaseModel
from ..enums.mentor_enums import DayOfWeek

class MentorAvailability(BaseModel):
    __tablename__ = "mentor_availability"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    mentor_profile_id = Column(UUID(as_uuid=True), ForeignKey("mentor_profiles.id"), nullable=False)
    day_of_week = Column(Enum(DayOfWeek), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    timezone = Column(String(50), nullable=False)
    is_recurring = Column(
        Boolean,
        default=True,
        comment="Indicates if the availability repeats on a regular basis",
    )
