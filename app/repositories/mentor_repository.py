from sqlalchemy.orm import Session
from fastapi import Depends
from .base_repository import BaseRepository
from ..models.mentor_profile import MentorProfile
from ..database import get_db

class MentorRepository(BaseRepository[MentorProfile]):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(db=db, model_class=MentorProfile)