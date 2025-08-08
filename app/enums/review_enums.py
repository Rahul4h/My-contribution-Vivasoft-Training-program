from enum import Enum

class ReviewStatus(Enum):
    VISIBLE = "visible"
    HIDDEN = "hidden"

class ReviewStatusColors(Enum):
    VISIBLE = "#10B981"
    HIDDEN = "#6B7280"