from enum import Enum

class VerificationStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class DayOfWeek(Enum):
    SUNDAY = "sunday"
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"

class DayOfWeekColors(Enum):
    SUNDAY = "#8B5CF6"
    MONDAY = "#3B82F6"
    TUESDAY = "#10B981"
    WEDNESDAY = "#F59E0B"
    THURSDAY = "#EF4444"
    FRIDAY = "#EC4899"
    SATURDAY = "#6B7280"