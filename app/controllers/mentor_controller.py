from typing import Dict, Any
from fastapi import Depends, HTTPException, status
from ..services.mentor_service import MentorService
from ..controllers.auth_controller import AuthController
from ..models.user import User
from ..schemas.mentor_profile import MentorProfileResponse

class MentorController:
    
    @staticmethod
    async def get_all_mentors(
        skip: int = 0, 
        limit: int = 10, 
        current_user: User = Depends(AuthController.get_current_active_user),
        mentor_service: MentorService = Depends()
    ) -> Dict[str, Any]:
        """Get all mentors with pagination."""
        try:
            mentors = mentor_service.get_all(skip=skip, limit=limit)
            return {"mentors": mentors, "count": len(mentors)}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve mentors: {str(e)}"
            )
    
    @staticmethod
    async def get_mentor_by_id(
        mentor_id: str, 
        current_user: User = Depends(AuthController.get_current_active_user),
        mentor_service: MentorService = Depends()
    ) -> MentorProfileResponse:
        """Get mentor by ID."""
        try:
            mentor = mentor_service.get_by_id(mentor_id)
            if not mentor:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Mentor not found"
                )
            return mentor
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve mentor: {str(e)}"
            )
    
    @staticmethod
    async def create_mentor(
        mentor_data: Dict[str, Any],
        current_user: User = Depends(AuthController.get_current_active_user),
        mentor_service: MentorService = Depends()
    ) -> MentorProfileResponse:
        """Create a new mentor profile."""
        try:
            mentor = mentor_service.create(mentor_data)
            return mentor
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid mentor data: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create mentor: {str(e)}"
            )
    
    @staticmethod
    async def update_mentor(
        mentor_id: str,
        mentor_data: Dict[str, Any],
        current_user: User = Depends(AuthController.get_current_active_user),
        mentor_service: MentorService = Depends()
    ) -> MentorProfileResponse:
        """Update an existing mentor profile."""
        try:
            mentor = mentor_service.update(mentor_id, mentor_data)
            if not mentor:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Mentor not found"
                )
            return mentor
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid mentor data: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update mentor: {str(e)}"
            )
    
    @staticmethod
    async def delete_mentor(
        mentor_id: str,
        current_user: User = Depends(AuthController.get_current_active_user),
        mentor_service: MentorService = Depends()
    ) -> Dict[str, str]:
        """Delete a mentor profile."""
        try:
            success = mentor_service.delete(mentor_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Mentor not found"
                )
            return {"message": "Mentor deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete mentor: {str(e)}"
            )