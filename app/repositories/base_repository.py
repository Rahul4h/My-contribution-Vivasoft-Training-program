from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi import Depends
from ..models.base_model import BaseModel as DBBaseModel

ModelType = TypeVar('ModelType', bound=DBBaseModel)

class BaseRepository(Generic[ModelType]):

    def __init__(self, db: Session = Depends(), model_class: Type[ModelType] = None):
        self.db = db
        self.model_class = model_class

    async def get_all(self) -> List[ModelType]:
        return self.db.query(self.model_class).all()

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        return self.db.query(self.model_class).filter(self.model_class.id == id).first()

    async def create(self, data: dict) -> ModelType:
        db_item = self.model_class(**data)
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    async def update(self, id: int, data: dict) -> Optional[ModelType]:
        db_item = await self.get_by_id(id)
        if db_item:
            for key, value in data.items():
                setattr(db_item, key, value)
            self.db.commit()
            self.db.refresh(db_item)
        return db_item
    
    async def delete(self, id: int) -> bool:
        db_item = await self.get_by_id(id)
        if db_item:
            self.db.delete(db_item)
            self.db.commit()
            return True
        return False
