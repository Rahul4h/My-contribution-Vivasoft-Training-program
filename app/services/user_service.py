from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .base_service import BaseService
from ..repositories.user_repository import UserRepository
from ..models.user import User
from ..schemas.user import UserCreate
from ..schemas.user_update import UserUpdate
from ..database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService(BaseService[User]):
    def __init__(self, db: Session = Depends(get_db)):
        repository = UserRepository(db)
        super().__init__(repository=repository)
    
    def get_by_email(self, email: str):
        return self.repository.get_by_email(email)
    
    def create(self, user_data: UserCreate) -> User:
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
        user_dict["hashed_password"] = pwd_context.hash(user_data.password)
        user_dict.pop("password")  # Remove plain password
        
        return self.repository.create(user_dict)
    
    def update(self, user_id: str, user_data: UserUpdate) -> User:
        # Get existing user
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Prepare update data
        update_dict = {}
        
        if user_data.email:
            # Check if email already exists (and it's not the same user)
            existing_user = self.repository.get_by_email(user_data.email)
            if existing_user and existing_user.id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            update_dict["email"] = user_data.email
        
        if user_data.username:
            # Check if username already exists (and it's not the same user)
            existing_user = self.repository.get_by_username(user_data.username)
            if existing_user and existing_user.id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
            update_dict["username"] = user_data.username
        
        if user_data.password:
            update_dict["hashed_password"] = pwd_context.hash(user_data.password)
        
        return self.repository.update(user, update_dict)