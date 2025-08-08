from enum import Enum

class UserRole(Enum):
    STUDENT = "student"
    MENTOR = "mentor"
    ADMIN = "admin"

class UserRoleColors(Enum):
    STUDENT = "#3B82F6"
    MENTOR = "#10B981"
    ADMIN = "#EF4444"

class OAuthProvider(Enum):
    GOOGLE = "google"
    GITHUB = "github"
    FACEBOOK = "facebook"

class OAuthProviderColors(Enum):
    GOOGLE = "#DB4437"
    GITHUB = "#333333"
    FACEBOOK = "#1877F2"