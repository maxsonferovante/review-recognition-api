from nest.core import Controller, Get, Post

from .recognition_service import RecognitionService
from .recognition_model import Recognition


@Controller("recognition")
class RecognitionController:

    def __init__(self, recognition_service: RecognitionService):
        self.service = service

    @Get("/")
    async def get_recognition(self):
        return await self.recognition_service.get_recognition()

    @Post("/")
    async def add_recognition(self, recognition: Recognition):
        return await self.recognition_service.add_recognition(recognition)
 