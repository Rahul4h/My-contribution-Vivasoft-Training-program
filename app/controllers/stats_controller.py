from typing import Dict, Any
from fastapi import Depends
from ..services.user_service import UserService
from ..services.mentor_service import MentorService
from ..services.category_service import CategoryService

class StatsController:
    
    @staticmethod
    async def get_platform_stats(
        user_service: UserService = Depends(),
        mentor_service: MentorService = Depends(),
        category_service: CategoryService = Depends()
    ) -> Dict[str, Any]:
        """Get platform statistics including user, mentor, and category counts."""
        users = user_service.get_all()
        mentors = mentor_service.get_all()
        categories = category_service.get_all()
        
        return {
            "total_users": len(users),
            "total_mentors": len(mentors),
            "total_categories": len(categories)
        }