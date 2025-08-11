from sqlalchemy.orm import Session
from fastapi import Depends
from .base_repository import BaseRepository
from ..models.subject import Subject
from ..database import get_db

class SubjectRepository(BaseRepository[Subject]):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(db=db, model_class=Subject)
    
    def get_by_category(self, category_id: str, skip: int = 0, limit: int = 100):
        return self.db.query(self.model_class).filter(
            self.model_class.category_id == category_id,
            self.model_class.is_deleted.is_(False)
        ).offset(skip).limit(limit).all()