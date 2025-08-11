from fastapi import Depends, HTTPException
from ..services.subject_service import SubjectService
from ..controllers.auth_controller import AuthController
from ..models.user import User
from ..schemas.subject import SubjectCreate, SubjectUpdate
from typing import List, Dict, Any

class SubjectController:
    
    @staticmethod
    async def get_all_subjects(
        current_user: User = Depends(AuthController.get_current_active_user),
        subject_service: SubjectService = Depends()
    ):
        subjects = subject_service.get_all()
        return {"subjects": subjects, "count": len(subjects)}
    
    @staticmethod
    async def create_subject(
        subject_data: SubjectCreate,
        current_user: User = Depends(AuthController.get_current_active_user),
        subject_service: SubjectService = Depends()
    ):
        subject = subject_service.create(subject_data)
        return subject
    
    @staticmethod
    async def update_subject(
        subject_id: str,
        subject_data: SubjectUpdate,
        current_user: User = Depends(AuthController.get_current_active_user),
        subject_service: SubjectService = Depends()
    ):
        subject = subject_service.update(subject_id, subject_data)
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        return subject
    
    @staticmethod
    async def delete_subject(
        subject_id: str,
        current_user: User = Depends(AuthController.get_current_active_user),
        subject_service: SubjectService = Depends()
    ):
        try:
            success = subject_service.delete(subject_id)
            if not success:
                raise HTTPException(status_code=404, detail="Subject not found")
            return {"message": "Subject deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to delete subject: {str(e)}")