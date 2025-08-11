from fastapi import Depends
from .base_service import BaseService
from ..repositories.category_repository import CategoryRepository
from ..models.category import Category

class CategoryService(BaseService[Category]):
    def __init__(self, repository: CategoryRepository = Depends()):
        super().__init__(repository=repository)