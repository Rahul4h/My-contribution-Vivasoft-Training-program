from fastapi import Depends
from ..services.base_service import BaseService

class BaseController:
    def __init__(self, service: BaseService = Depends()):
        self.service = service
