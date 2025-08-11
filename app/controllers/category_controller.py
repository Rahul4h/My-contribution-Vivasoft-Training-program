from typing import Dict, Any
from fastapi import Depends, HTTPException, status
from ..services.category_service import CategoryService
from ..services.subject_service import SubjectService
from ..controllers.auth_controller import AuthController
from ..models.user import User
from ..schemas.category import CategoryResponse

class CategoryController:
    
    @staticmethod
    async def get_all_categories(
        current_user: User = Depends(AuthController.get_current_active_user),
        category_service: CategoryService = Depends()
    ) -> Dict[str, Any]:
        categories = category_service.get_all()
        return {"categories": categories, "count": len(categories)}
    
    @staticmethod
    async def get_category_subjects(
        category_id: str, 
        current_user: User = Depends(AuthController.get_current_active_user),
        subject_service: SubjectService = Depends()
    ) -> Dict[str, Any]:
        subjects = subject_service.get_by_category(category_id)
        return {"subjects": subjects, "count": len(subjects)}
    
    @staticmethod
    async def create_category(
        category_data: Dict[str, Any],
        current_user: User = Depends(AuthController.get_current_active_user),
        category_service: CategoryService = Depends()
    ) -> CategoryResponse:
        try:
            category = category_service.create(category_data)
            return category
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to create category: {str(e)}")
    
    @staticmethod
    async def update_category(
        category_id: str,
        category_data: Dict[str, Any],
        current_user: User = Depends(AuthController.get_current_active_user),
        category_service: CategoryService = Depends()
    ) -> CategoryResponse:
        try:
            category = category_service.update(category_id, category_data)
            if not category:
                raise HTTPException(status_code=404, detail="Category not found")
            return category
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to update category: {str(e)}")
    
    @staticmethod
    async def delete_category(
        category_id: str,
        current_user: User = Depends(AuthController.get_current_active_user),
        category_service: CategoryService = Depends()
    ) -> Dict[str, str]:
        try:
            success = category_service.delete(category_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found"
                )
            return {"message": "Category deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete category: {str(e)}"
            )