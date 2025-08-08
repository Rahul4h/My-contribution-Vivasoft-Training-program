from sqlalchemy import Column, String, ForeignKey, Enum, Time, Boolean
from sqlalchemy.dialects.postgresql import UUID
from .base_model import BaseModel
from ..enums import DayOfWeek
import uuid


class MentorAvailability(BaseModel):
    __tablename__ = "mentor_availability"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    mentorId = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    dayOfWeek = Column(Enum(DayOfWeek), nullable=False)
    startTime = Column(Time, nullable=False)
    endTime = Column(Time, nullable=False)
    timezone = Column(String(50), nullable=False)
    isRecurring = Column(
        Boolean,
        default=True,
        comment="Indicates if the availability repeats on a regular basis",
    )
