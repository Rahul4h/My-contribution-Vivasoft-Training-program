from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .base_service import BaseService
from ..repositories.subject_repository import SubjectRepository
from ..models.subject import Subject
from ..schemas.subject import SubjectCreate, SubjectUpdate
from ..database import get_db

class SubjectService(BaseService[Subject]):
    def __init__(self, db: Session = Depends(get_db)):
        repository = SubjectRepository(db)
        super().__init__(repository=repository)
    
    def get_by_category(self, category_id: str, skip: int = 0, limit: int = 100):
        return self.repository.get_by_category(category_id, skip, limit)
    
    def create(self, subject_data: SubjectCreate) -> Subject:
        subject_dict = subject_data.dict()
        return self.repository.create(subject_dict)
    
    def update(self, subject_id: str, subject_data: SubjectUpdate) -> Subject:
        subject = self.repository.get_by_id(subject_id)
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subject not found"
            )
        
        update_dict = {k: v for k, v in subject_data.dict().items() if v is not None}
        return self.repository.update(subject_id, update_dict)