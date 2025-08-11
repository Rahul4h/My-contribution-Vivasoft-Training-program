from sqlalchemy.orm import Session
from fastapi import Depends
from .base_repository import BaseRepository
from ..models.category import Category
from ..database import get_db

class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(db=db, model_class=Category)