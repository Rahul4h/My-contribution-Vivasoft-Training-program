from typing import Generic, TypeVar, List, Optional, Dict, Any
from fastapi import Depends
from ..interfaces import ServiceInterface, RepositoryInterface
from ..models.base_model import BaseModel as DBBaseModel

ModelType = TypeVar('ModelType', bound=DBBaseModel)

class BaseService(ServiceInterface[ModelType], Generic[ModelType]):
    def __init__(self, repository: RepositoryInterface[ModelType] = Depends()):
        self.repository = repository

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return await self.repository.get_all(skip, limit)

    async def get_by_id(self, id: str) -> Optional[ModelType]:
        return await self.repository.get_by_id(id)

    async def create(self, data: Dict[str, Any]) -> ModelType:
        return await self.repository.create(data)

    async def update(self, id: str, data: Dict[str, Any]) -> Optional[ModelType]:
        return await self.repository.update(id, data)
    
    async def delete(self, id: str) -> bool:
        return await self.repository.delete(id)
