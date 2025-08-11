from typing import Generic, TypeVar, Type, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import Depends
from datetime import datetime
from ..database import get_db
from ..interfaces import RepositoryInterface
from ..models.base_model import BaseModel as DBBaseModel

ModelType = TypeVar('ModelType', bound=DBBaseModel)

class BaseRepository(RepositoryInterface[ModelType], Generic[ModelType]):

    def __init__(self, db: Session = Depends(get_db), model_class: Type[ModelType] = None):
        self.db = db
        self.model_class = model_class

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return self.db.query(self.model_class).filter(self.model_class.is_deleted == False).offset(skip).limit(limit).all()

    def get_by_id(self, id: str) -> Optional[ModelType]:
        return self.db.query(self.model_class).filter(self.model_class.id == id, self.model_class.is_deleted == False).first()

    def create(self, data: Dict[str, Any]) -> ModelType:
        db_item = self.model_class(**data)
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def update(self, id: str, data: Dict[str, Any]) -> Optional[ModelType]:
        db_item = self.get_by_id(id)
        if not db_item:
            raise ValueError(f"Item with id {id} not found.")
        for key, value in data.items():
            setattr(db_item, key, value)
        db_item.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
    
    def delete(self, id: str) -> bool:
        db_item = self.db.query(self.model_class).filter(self.model_class.id == id).first()
        if db_item:
            self.db.delete(db_item)
            self.db.commit()
            return True
        return False
    
    def soft_delete(self, id: str) -> bool:
        db_item = self.get_by_id(id)
        if db_item:
            db_item.is_deleted = True
            db_item.deleted_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
