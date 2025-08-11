from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import secrets
from .base_repository import BaseRepository
from ..models.user import User
from ..database import get_db

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(db=db, model_class=User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def create(self, data: Dict[str, Any]) -> User:
        db_user = User(**data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update(self, user: User, data: Dict[str, Any]) -> User:
        for key, value in data.items():
            setattr(user, key, value)
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_all_users(self, skip: int = 0, limit: int = 100):
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def create_reset_token(self, user: User) -> str:
        token = secrets.token_urlsafe(32)
        user.reset_token = token
        user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        self.db.commit()
        return token
    
    def get_by_reset_token(self, token: str) -> Optional[User]:
        return self.db.query(User).filter(
            User.reset_token == token,
            User.reset_token_expires > datetime.utcnow()
        ).first()
    
    def clear_reset_token(self, user: User):
        user.reset_token = None
        user.reset_token_expires = None
        self.db.commit()