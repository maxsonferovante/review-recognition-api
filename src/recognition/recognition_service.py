from .recognition_model import Recognition
from .recognition_entity import Recognition as RecognitionEntity
from nest.core.decorators.database import db_request_handler
from nest.core import Injectable


@Injectable
class RecognitionService:

    @db_request_handler
    async def add_recognition(self, recognition: Recognition):
        new_recognition = RecognitionEntity(
            created_at = recognition.created_at,
            file_name = recognition.file_name,
            id = recognition.id
        )
        await new_recognition.save()
        return new_recognition.id

    @db_request_handler
    async def get_recognition(self):
        return await RecognitionEntity.find_all().to_list()
