from typing import List, Dict, Any
from fastapi import APIRouter, Depends, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..controllers.user_controller import UserController
from ..controllers.mentor_controller import MentorController
from ..controllers.category_controller import CategoryController
from ..controllers.subject_controller import SubjectController
from ..controllers.stats_controller import StatsController
from ..controllers.auth_controller import AuthController
from ..schemas.user import UserResponse, Token, UserCreate
from ..schemas.user_update import UserUpdate
from ..schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from ..schemas.subject import SubjectCreate, SubjectUpdate, SubjectResponse
from ..schemas.mentor_profile import MentorProfileCreate, MentorProfileUpdate, MentorProfileResponse
from jose import jwt
from datetime import datetime, timedelta
from ..config.settings import get_settings

router = APIRouter()

@router.get("/")
async def root():
    """🏠 Welcome endpoint"""
    return {"message": "Welcome to FastAPI Mentorship Platform"}

@router.get("/health")
async def health_check():
    """💚 Health check endpoint"""
    return {"status": "healthy", "database": "connected"}

# Authentication Routes
@router.post("/register", response_model=Token)
def register(response: dict = Depends(AuthController.register)):
    """
    📝 Register - Create new user account
    
    - **email**: User's email address
    - **username**: Unique username
    - **password**: Secure password (min 8 characters)
    
    Returns access token and user info
    """
    return response

@router.post("/login", response_model=Token)
def login(response: dict = Depends(AuthController.login)):
    """
    🔑 Login - Authenticate user and get token
    
    - **email**: User's email address
    - **password**: User's password
    
    Returns access token and user info
    """
    return response

@router.post("/forgot-password")
def forgot_password(response: dict = Depends(AuthController.forgot_password)):
    """
    🔄 Forgot Password - Request password reset
    
    - **email**: User's email address
    
    Sends password reset token (in production, would email a reset link)
    """
    return response

@router.post("/reset-password")
def reset_password(response: dict = Depends(AuthController.reset_password)):
    """
    🔄 Reset Password - Reset password with token
    
    - **token**: Password reset token
    - **new_password**: New password (min 8 characters)
    
    Resets password if token is valid
    """
    return response

@router.get("/profile", response_model=UserResponse)
async def get_profile(user: UserResponse = Depends(AuthController.get_user_profile)):
    """
    👤 Profile - Get current user profile
    
    Requires authentication token
    
    Returns user profile information
    """
    return user

@router.post("/refresh", response_model=Token)
def refresh_token(response: dict = Depends(AuthController.refresh_token)):
    """
    🔄 Refresh Token - Generate new access token
    
    - **refresh_token**: Valid refresh token
    
    Returns new access and refresh tokens
    """
    return response

@router.get("/token-info")
def get_token_info(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """
    🔍 Token Info - Get detailed information about the provided token
    
    Analyzes the JWT token and returns:
    - Creation time
    - Expiration time
    - Time remaining
    - Algorithm used
    - Token type
    - User email
    """
    settings = get_settings()
    token = credentials.credentials
    
    try:
        # Decode token without verification to get payload
        payload = jwt.get_unverified_claims(token)
        
        # Extract information
        user_email = payload.get("sub")
        exp_timestamp = payload.get("exp")
        token_type = payload.get("type", "access")
        
        # Calculate times
        exp_datetime = datetime.fromtimestamp(exp_timestamp) if exp_timestamp else None
        current_time = datetime.now()
        
        # Calculate creation time (approximate)
        if token_type == "access":
            created_datetime = exp_datetime - timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) if exp_datetime else None
        else:
            created_datetime = exp_datetime - timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES) if exp_datetime else None
        
        # Calculate time remaining
        time_remaining = None
        is_expired = False
        if exp_datetime:
            time_remaining = exp_datetime - current_time
            is_expired = current_time > exp_datetime
        
        return {
            "token_type": token_type,
            "user_email": user_email,
            "algorithm": settings.ALGORITHM,
            "created_at": created_datetime.isoformat() if created_datetime else None,
            "expires_at": exp_datetime.isoformat() if exp_datetime else None,
            "current_time": current_time.isoformat(),
            "is_expired": is_expired,
            "time_remaining_seconds": int(time_remaining.total_seconds()) if time_remaining and not is_expired else 0,
            "time_remaining_minutes": int(time_remaining.total_seconds() / 60) if time_remaining and not is_expired else 0,
            "token_length": len(token),
            "payload": payload
        }
        
    except Exception as e:
        return {
            "error": "Invalid token",
            "details": str(e)
        }

# User Routes
@router.get("/users", response_model=List[UserResponse])
async def get_all_users(users: list[UserResponse] = Depends(AuthController.get_all_users)):
    """
    👥 Get All Users - Retrieve all users from the database

    Note: Requires authentication. You must provide a valid Authorization: Bearer <token> header.
    """
    return users

@router.get("/users/{user_id}")
async def get_user(user = Depends(UserController.get_user_by_id)):
    """
    👤 Get User by ID - Retrieve specific user
    
    Requires JWT authentication
    """
    return user

@router.post("/users")
async def create_user(user_data: UserCreate, user = Depends(UserController.create_user)):
    """
    ➕ Create User - Create a new user
    
    Required fields:
    - **email**: Valid email address
    - **username**: Unique username
    - **password**: Secure password (min 8 characters)
    
    Requires JWT authentication
    """
    return user

@router.put("/users/{user_id}")
async def update_user(user_id: str, user_data: UserUpdate, user = Depends(UserController.update_user)):
    """
    ✏️ Update User - Update existing user
    
    Optional fields to update:
    - **email**: Valid email address
    - **username**: Unique username
    - **password**: New password (min 8 characters)
    
    Requires JWT authentication
    """
    return user

@router.delete("/users/{user_id}")
async def delete_user(response: dict = Depends(UserController.delete_user)):
    """
    🗑️ Delete User - Delete existing user
    
    Requires JWT authentication
    """
    return response

# Mentor Routes
@router.get("/mentors")
async def get_mentors(response: dict = Depends(MentorController.get_all_mentors)):
    """
    🎓 Get All Mentors - Retrieve all mentors from the database
    
    Requires JWT authentication
    """
    return response

@router.get("/mentors/{mentor_id}")
async def get_mentor(mentor = Depends(MentorController.get_mentor_by_id)):
    """
    👨‍🏫 Get Mentor by ID - Retrieve specific mentor
    
    Requires JWT authentication
    """
    return mentor

@router.post("/mentors")
async def create_mentor(mentor_data: MentorProfileCreate, mentor = Depends(MentorController.create_mentor)):
    """
    ➕ Create Mentor - Create a new mentor profile
    
    Required fields:
    - **user_id**: UUID of the user becoming a mentor
    
    Optional fields:
    - **about**: Description about the mentor
    - **hourly_rate**: Hourly rate in USD (must be >= 0)
    - **is_available**: Whether mentor is available (default: true)
    - **hiring_card_url**: URL to mentor's hiring card
    
    Requires JWT authentication
    """
    return mentor

@router.put("/mentors/{mentor_id}")
async def update_mentor(mentor_data: MentorProfileUpdate, mentor = Depends(MentorController.update_mentor)):
    """
    ✏️ Update Mentor - Update existing mentor
    
    Optional fields to update:
    - **about**: Description about the mentor
    - **hourly_rate**: Hourly rate in USD (must be >= 0)
    - **is_available**: Whether mentor is available
    - **hiring_card_url**: URL to mentor's hiring card
    
    Requires JWT authentication
    """
    return mentor

@router.delete("/mentors/{mentor_id}")
async def delete_mentor(response: dict = Depends(MentorController.delete_mentor)):
    """
    🗑️ Delete Mentor - Delete existing mentor
    
    Requires JWT authentication
    """
    return response

# Category Routes
@router.get("/categories")
async def get_categories(response: dict = Depends(CategoryController.get_all_categories)):
    """
    Get All Categories - Retrieve all categories
    
    Requires JWT authentication
    """
    return response

@router.post("/categories")
async def create_category(category_data: CategoryCreate, category = Depends(CategoryController.create_category)):
    """
    📂 Create Category - Create a new category
    
    Required fields:
    - **name**: Category name (max 100 characters)
    
    Optional fields:
    - **description**: Category description
    
    Requires JWT authentication
    """
    return category

@router.put("/categories/{category_id}")
async def update_category(category_data: CategoryUpdate, category = Depends(CategoryController.update_category)):
    """
    ✏️ Update Category - Update existing category
    
    Optional fields to update:
    - **name**: Category name (max 100 characters)
    - **description**: Category description
    
    Requires JWT authentication
    """
    return category

@router.delete("/categories/{category_id}")
async def delete_category(response: dict = Depends(CategoryController.delete_category)):
    """
    Delete Category - Delete existing category
    
    Requires JWT authentication
    """
    return response

@router.get("/categories/{category_id}/subjects")
async def get_category_subjects(response: dict = Depends(CategoryController.get_category_subjects)):
    """
    Get Category Subjects - Retrieve subjects by category
    
    Requires JWT authentication
    """
    return response

# Subject Routes
@router.get("/subjects")
async def get_subjects(response: dict = Depends(SubjectController.get_all_subjects)):
    """
    Get All Subjects - Retrieve all subjects
    
    Requires JWT authentication
    """
    return response

@router.post("/subjects")
async def create_subject(subject_data: SubjectCreate, subject = Depends(SubjectController.create_subject)):
    """
    📚 Create Subject - Create a new subject
    
    Required fields:
    - **name**: Subject name (max 100 characters)
    - **category_id**: UUID of the category this subject belongs to
    
    Optional fields:
    - **description**: Subject description
    
    Requires JWT authentication
    """
    return subject

@router.put("/subjects/{subject_id}")
async def update_subject(subject_data: SubjectUpdate, subject = Depends(SubjectController.update_subject)):
    """
    ✏️ Update Subject - Update existing subject
    
    Optional fields to update:
    - **name**: Subject name (max 100 characters)
    - **description**: Subject description
    - **category_id**: UUID of the category this subject belongs to
    
    Requires JWT authentication
    """
    return subject

@router.delete("/subjects/{subject_id}")
async def delete_subject(response: dict = Depends(SubjectController.delete_subject)):
    """
    Delete Subject - Delete existing subject
    
    Requires JWT authentication
    """
    return response

# Stats Routes
@router.get("/stats")
async def get_stats(response: dict = Depends(StatsController.get_platform_stats)):
    """
    Get Platform Statistics - Retrieve platform statistics
    
    Requires JWT authentication
    """
    return response