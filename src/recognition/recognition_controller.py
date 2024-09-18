from nest.core import Controller, Get, Post
from fastapi import UploadFile
from .recognition_service import RecognitionService
from .recognition_model import Recognition
from .recognition_validation import validate_file_type, validate_file_size
from .recognition_exceptions import InternalServerError

@Controller("recognition")
class RecognitionController:

    def __init__(self, recognition_service: RecognitionService):
        self.service = service

    @Get("/")
    async def get_recognition(self):
        return await self.recognition_service.get_recognition()

    @Post("/upload")
    async def add_recognition(self, file: UploadFile):        
        validate_file_size(file)
        validate_file_type(file)
            
        file_name = file.filename        
        recognition = Recognition(file_name=file_name)        
        recognition_id = await self.recognition_service.add_recognition(recognition)
        return {
                "recognition_id": recognition_id,
                "file": file.filename,
                "size": len(file.file.read()),
                "extension": file.filename.split(".")[-1]
            }