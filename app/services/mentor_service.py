from fastapi import Depends
from .base_service import BaseService
from ..repositories.mentor_repository import MentorRepository
from ..models.mentor_profile import MentorProfile

class MentorService(BaseService[MentorProfile]):
    def __init__(self, repository: MentorRepository = Depends()):
        super().__init__(repository=repository)