from .recognition_model import Recognition
from .recognition_entity import Recognition as RecognitionEntity
from .recognition_entity import mongo_recognition_to_pydantic
from nest.core.decorators.database import db_request_handler
from nest.core import Injectable


@Injectable
class RecognitionService:
    
    def __init__(self):
        pass
    
    @db_request_handler
    async def add_recognition(self, recognition: Recognition):
        new_recognition = RecognitionEntity(
            created_at = recognition.created_at,
            file_name = recognition.file_name,
            extension = recognition.extension,
            status = recognition.status
        )
        await new_recognition.save()
        return new_recognition.id

    @db_request_handler
    async def get_recognition(self):
        result = await RecognitionEntity.find_all().to_list()
        list_recognition = []
            
        for recognitionDocument in result:
            recognitionDict = mongo_recognition_to_pydantic(recognitionDocument)                
            list_recognition.append(Recognition(**recognitionDict))  
            
        return list_recognition                

    @db_request_handler
    async def get_recognition_by_id(self, id: str):
        result = await RecognitionEntity.get(id)
        if result:
            recognitionDict = mongo_recognition_to_pydantic(result)
            return Recognition(**recognitionDict)
        return None