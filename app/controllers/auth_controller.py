from typing import Dict, Any, List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from pydantic import EmailStr
from ..schemas.user import UserCreate, UserLogin, TokenData, PasswordReset, PasswordResetConfirm, UserResponse, RefreshToken
from ..services.auth_service import AuthService
from ..repositories.user_repository import UserRepository
from ..database import get_db
from ..config.settings import get_settings
from ..models.user import User

# HTTP Bearer scheme for token authentication
bearer_scheme = HTTPBearer()
settings = get_settings()

class AuthController:
    """
    Auth Controller - Handles authentication requests
    """
    @staticmethod
    def get_service(db: Session = Depends(get_db)) -> AuthService:
        """
        Get Service - Create and return auth service instance
        """
        repository = UserRepository(db)
        return AuthService(repository)
    
    @staticmethod
    def register(
        user_data: UserCreate, 
        service: AuthService = Depends(get_service)
    ) -> Dict[str, Any]:
        """
        Register - Create new user account
        """
        return service.register_user(user_data)
    
    @staticmethod
    def login(
        user_data: UserLogin, 
        service: AuthService = Depends(get_service)
    ) -> Dict[str, Any]:
        """
        Login - Authenticate user and return token
        """
        return service.login_user(user_data)
    
    @staticmethod
    def forgot_password(
        password_reset: PasswordReset, 
        service: AuthService = Depends(get_service)
    ) -> Dict[str, str]:
        """
        Forgot Password - Send password reset token
        """
        return service.forgot_password(password_reset.email)
    
    @staticmethod
    def reset_password(
        reset_data: PasswordResetConfirm, 
        service: AuthService = Depends(get_service)
    ) -> Dict[str, str]:
        """
        Reset Password - Reset password using token
        """
        return service.reset_password(reset_data.token, reset_data.new_password)
    
    @staticmethod
    async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        repository: UserRepository = Depends(lambda db=Depends(get_db): UserRepository(db))
    ) -> User:
        """
        Get Current User - Get authenticated user from token
        """
        # Define the exception for authentication failures
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            # Decode JWT token
            payload = jwt.decode(
                credentials.credentials, 
                settings.SECRET_KEY, 
                algorithms=[settings.ALGORITHM]
            )
            
            # Extract email from token
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
                
        except JWTError:
            raise credentials_exception
            
        # Get user from database
        user = repository.get_by_email(email)
        
        if user is None:
            raise credentials_exception
            
        return user
    
    @staticmethod
    async def get_current_active_user(
        current_user: User = Depends(get_current_user)
    ) -> User:
        """
        Get Current Active User - Check if user is active
        """
        if not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Inactive user"
            )
        return current_user
    
    @staticmethod
    async def get_user_profile(
        current_user: User = Depends(get_current_active_user)
    ) -> UserResponse:
        """
        Get User Profile - Return current user profile
        """
        return UserResponse.model_validate(current_user)
    
    @staticmethod
    async def get_all_users(
        current_user: User = Depends(get_current_active_user),
        repository: UserRepository = Depends(lambda db=Depends(get_db): UserRepository(db))
    ) -> List[UserResponse]:
        """
        Get All Users - Return all users as UserResponse list
        """
        users = repository.get_all_users()
        return [UserResponse.model_validate(user) for user in users]
    
    @staticmethod
    def refresh_token(
        refresh_data: RefreshToken,
        service: AuthService = Depends(get_service)
    ) -> Dict[str, Any]:
        """
        Refresh Token - Generate new access token using refresh token
        """
        return service.refresh_access_token(refresh_data.refresh_token)