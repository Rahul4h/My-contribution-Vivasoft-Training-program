from typing import Generic, TypeVar, List, Optional, Type
from fastapi import Depends
from ..repositories.base_repository import BaseRepository
from ..models.base_model import BaseModel as DBBaseModel

ModelType = TypeVar('ModelType', bound=DBBaseModel)

class BaseService(Generic[ModelType]):
    def __init__(self, repository: BaseRepository[ModelType] = Depends()):
        self.repository = repository

    async def get_all(self) -> List[ModelType]:
        return await self.repository.get_all()

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        return await self.repository.get_by_id(id)

    async def create(self, data: dict) -> ModelType:
        return await self.repository.create(data)

    async def update(self, id: int, data: dict) -> Optional[ModelType]:
        return await self.repository.update(id, data)
    
    async def delete(self, id: int) -> bool:
        return await self.repository.delete(id)
