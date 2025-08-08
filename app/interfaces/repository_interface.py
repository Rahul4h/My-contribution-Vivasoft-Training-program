from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Dict, Any

ModelType = TypeVar('ModelType')

class RepositoryInterface(ABC, Generic[ModelType]):

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        pass
    
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[ModelType]:
        pass
    
    @abstractmethod
    async def create(self, data: Dict[str, Any]) -> ModelType:
        pass
    
    @abstractmethod
    async def update(self, id: str, data: Dict[str, Any]) -> Optional[ModelType]:
        pass
    
    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass
    
    @abstractmethod
    async def soft_delete(self, id: str) -> bool:
        pass