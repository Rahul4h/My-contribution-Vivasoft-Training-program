from enum import Enum

class SessionType(Enum):
    VIDEO_CALL = "video_call"
    CHAT = "chat"
    IN_PERSON = "in_person"

class SessionTypeColors(Enum):
    VIDEO_CALL = "#10B981"
    CHAT = "#F59E0B"
    IN_PERSON = "#6B7280"