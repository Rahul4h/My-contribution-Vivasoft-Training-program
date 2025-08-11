from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate, UserLogin, TokenData, RefreshToken
from ..config.settings import get_settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()

class AuthService:
    """
    Auth Service - Handles authentication and security operations
    """
    def __init__(self, repository: UserRepository):
        """
        Constructor - Initialize with user repository
        """
        self.repository = repository
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify Password - Check if password matches hash
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """
        Get Password Hash - Create hash from password
        """
        return pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create Access Token - Generate JWT token
        """
        to_encode = data.copy()
        
        now = datetime.utcnow()
        # Set expiration time
        if expires_delta:
            expire = now + expires_delta
        else:
            expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            
        to_encode.update({"exp": expire, "type": "access"})
        
        # Create JWT token
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
        
        return encoded_jwt
    
    def create_refresh_token(self, data: dict) -> str:
        """
        Create Refresh Token - Generate JWT refresh token
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "type": "refresh"})
        
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        
        return encoded_jwt
    
    def register_user(self, user_data: UserCreate) -> dict:
        """
        Register User - Create new user account
        """
        # Check if email already exists
        if self.repository.get_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
            
        # Check if username already exists
        if self.repository.get_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Create user with hashed password
        user_dict = user_data.dict()
        user_dict["hashed_password"] = self.get_password_hash(user_data.password)
        user_dict.pop("password")  # Remove plain password
        
        user = self.repository.create(user_dict)
        
        # Generate tokens
        access_token = self.create_access_token(data={"sub": user.email})
        refresh_token = self.create_refresh_token(data={"sub": user.email})
        
        # Store refresh token in database
        self.repository.update(user, {"refresh_token": refresh_token})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_id": str(user.id),
            "email": user.email
        }
    
    def login_user(self, user_data: UserLogin) -> dict:
        """
        Login User - Authenticate user and return token
        """
        # Find user by email
        user = self.repository.get_by_email(user_data.email)
        
        # Check if user exists and password is correct
        if not user or not self.verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        # Generate tokens
        access_token = self.create_access_token(data={"sub": user.email})
        refresh_token = self.create_refresh_token(data={"sub": user.email})
        
        # Store refresh token in database
        self.repository.update(user, {"refresh_token": refresh_token})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_id": str(user.id),
            "email": user.email
        }
    
    def forgot_password(self, email: str) -> dict:
        """
        Forgot Password - Send password reset token
        """
        # Find user by email
        user = self.repository.get_by_email(email)
        
        # Check if user exists
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        # Generate reset token
        token = self.repository.create_reset_token(user)
        
        # In a real application, send email with reset link
        # For this example, we'll just return the token
        return {
            "message": "Password reset token generated",
            "token": token  # In production, don't return this directly
        }
    
    def reset_password(self, token: str, new_password: str) -> dict:
        """
        Reset Password - Reset password using token
        """
        # Validate password strength
        if len(new_password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long"
            )
            
        # Find user by reset token
        user = self.repository.get_by_reset_token(token)
        
        # Check if token is valid
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired token"
            )
            
        # Update password
        user.hashed_password = self.get_password_hash(new_password)
        
        # Clear reset token
        self.repository.clear_reset_token(user)
        
        # Save changes
        self.repository.update(user, {"hashed_password": user.hashed_password})
        
        return {"message": "Password reset successful"}
    
    def refresh_access_token(self, refresh_token: str) -> dict:
        """
        Refresh Access Token - Generate new access token using refresh token
        """
        try:
            # Decode refresh token
            payload = jwt.decode(
                refresh_token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            
            email: str = payload.get("sub")
            token_type: str = payload.get("type")
            
            if email is None or token_type != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token"
                )
                
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Find user and verify refresh token exists in database
        user = self.repository.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
            
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is inactive"
            )
            
        # Check if refresh token matches the one stored in database
        if user.refresh_token != refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Generate new tokens
        new_access_token = self.create_access_token(data={"sub": user.email})
        new_refresh_token = self.create_refresh_token(data={"sub": user.email})
        
        # Update refresh token in database
        self.repository.update(user, {"refresh_token": new_refresh_token})
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }