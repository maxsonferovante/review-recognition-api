from typing import List
from nest.core import Controller, Get, Post
from fastapi import UploadFile
from .recognition_service import RecognitionService
from .recognition_model import Recognition
from .recognition_exceptions import
from .recognition_http_response import AcceptedResponse, CompletedResponse

@Controller("recognition")
class RecognitionController:

    def __init__(self, recognition_service: RecognitionService):
        self.recognition_service = recognition_service
          
    @Get("/")
    async def get_recognition(self) -> List[Recognition]:
        response = await self.recognition_service.get_recognition()
        return CompletedResponse(content=response)
        
    @Post("/upload")
    async def add_recognition(self, file: UploadFile) -> AcceptedResponse:                              
        recognition = await self.recognition_service.add_recognition(file)        
        return AcceptedResponse(recognition)