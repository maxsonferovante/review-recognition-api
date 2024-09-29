from typing import List
from nest.core import Controller, Get, Post
from fastapi import UploadFile, BackgroundTasks
from src.modules.character_recognition.character_recognition_service import CharacterRecognitionService
from src.modules.character_recognition.character_recognition_model import ProcessingRecognition, CompletedRecognition
from .recognition_service import RecognitionService
from .recognition_model import Recognition, RecognitionStatus
from .recognition_validation import validate_file_type, validate_file_size
from .recognition_exceptions import RecognitionNotFound
from .recognition_http_response import AcceptedResponse, ProcessingResponse, CompletedResponse

@Controller("recognition")
class RecognitionController:

    def __init__(self, recognition_service: RecognitionService,character_recognition_service: CharacterRecognitionService):
        self.recognition_service = recognition_service
        self.character_recognition_service = character_recognition_service
          
    @Get("/")
    async def get_recognition(self) -> List[Recognition]:
        return await self.recognition_service.get_recognition()
    
    @Get("/{id}/status")
    async def get_recognition_by_id(self, id: str) -> ProcessingRecognition or RecognitionNotFound:

        recognition_status = self.character_recognition_service.get_status(id)
        if not recognition_status:
            raise RecognitionNotFound()
        
        await self.recognition_service.update_status_recognition(recognition_status["id"], recognition_status["status"])
                
        return ProcessingResponse(content=recognition_status)
    
    @Get("/{id}/results")
    async def get_recognition_results_by_id(self, id: str) -> CompletedRecognition or RecognitionNotFound:
        recognition = self.character_recognition_service.get_results(id)
        if not recognition:
            raise RecognitionNotFound()
        return CompletedResponse(content=recognition)
    
    @Post("/upload")
    async def add_recognition(self, file: UploadFile, background_tasks: BackgroundTasks) -> AcceptedResponse:        
        validate_file_size(file)
        validate_file_type(file)
                      
        recognition = Recognition(
            file_name=file.filename, 
            extension=file.filename.split(".")[-1])        
    
        recognition.id = await self.recognition_service.add_recognition(recognition)
        background_tasks.add_task(self.character_recognition_service.run, recognition.id)
        
        return AcceptedResponse(recognition)