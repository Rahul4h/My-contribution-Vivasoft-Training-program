from typing import Dict, Any
from fastapi import Depends, HTTPException, status
from ..services.user_service import UserService
from ..controllers.auth_controller import AuthController
from ..models.user import User
from ..schemas.user import UserCreate, UserResponse
from ..schemas.user_update import UserUpdate

class UserController:
    
    @staticmethod
    async def get_all_users(
        skip: int = 0, 
        limit: int = 10, 
        current_user: User = Depends(AuthController.get_current_active_user),
        user_service: UserService = Depends()
    ) -> Dict[str, Any]:
        """Get all users with pagination."""
        try:
            users = user_service.get_all(skip=skip, limit=limit)
            return {"users": users, "count": len(users)}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve users: {str(e)}"
            )
    
    @staticmethod
    async def get_user_by_id(
        user_id: str, 
        current_user: User = Depends(AuthController.get_current_active_user),
        user_service: UserService = Depends()
    ) -> UserResponse:
        """Get user by ID."""
        try:
            user = user_service.get_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            return user
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve user: {str(e)}"
            )
    
    @staticmethod
    async def create_user(
        user_data: UserCreate,
        current_user: User = Depends(AuthController.get_current_active_user),
        user_service: UserService = Depends()
    ) -> UserResponse:
        """Create a new user."""
        try:
            user = user_service.create(user_data)
            return user
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid user data: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create user: {str(e)}"
            )
    
    @staticmethod
    async def update_user(
        user_id: str,
        user_data: UserUpdate,
        current_user: User = Depends(AuthController.get_current_active_user),
        user_service: UserService = Depends()
    ) -> UserResponse:
        """Update an existing user."""
        try:
            user = user_service.update(user_id, user_data)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            return user
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid user data: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update user: {str(e)}"
            )
    
    @staticmethod
    async def delete_user(
        user_id: str,
        current_user: User = Depends(AuthController.get_current_active_user),
        user_service: UserService = Depends()
    ) -> Dict[str, str]:
        """Delete a user."""
        try:
            success = user_service.delete(user_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            return {"message": "User deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete user: {str(e)}"
            )