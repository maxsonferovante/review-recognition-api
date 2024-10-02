from .recognition_model import Recognition
from .recognition_entity import Recognition as RecognitionEntity, RecognitionStatus
from .recognition_entity import mongo_recognition_to_pydantic

from src.modules.character_recognition.character_recognition_service import CharacterRecognitionService
from src.providers.black_blaze_bucket_file import BlackBlazeBucketFile

from nest.core.decorators.database import db_request_handler
from nest.core import Injectable

from fastapi import UploadFile

@Injectable
class RecognitionService:
    
    def __init__(self, character_recognition_service: CharacterRecognitionService,
                        updateBucketFile: BlackBlazeBucketFile):
        self.character_recognition_service = character_recognition_service
        self.updateBucketFile = updateBucketFile
    
    @db_request_handler
    async def add_recognition(self, file: UploadFile) -> Recognition:
        recognition = Recognition(
            file_name=file.filename, 
            extension=file.filename.split(".")[-1])        
        
        new_recognition = RecognitionEntity(
            created_at = recognition.created_at,
            file_name = recognition.file_name,
            extension = recognition.extension,
            status = recognition.status
        )
        await new_recognition.save()
        recognition.id = new_recognition.id
        # self.character_recognition_service.save_file_in_disk(
        #     file = file,
        #     file_name=recognition.file_name,
        #     path_to_save=recognition.id
        # )
        
        url = await self.updateBucketFile.upload_file(file=file, recognition_id=recognition.id, file_name=recognition.file_name)
        
        update_recognition = await RecognitionEntity.get(recognition.id)
        update_recognition.data = {"url": url}
        await update_recognition.save()
        # self.character_recognition_service.run(id=recognition.id)
        
        # await self.updateBucketFile.download_file(recognition_id=recognition.id, file_name=recognition.file_name)
        return recognition

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
    
    @db_request_handler
    async def update_status_recognition(self, id: str, status: str):        
        if status == RecognitionStatus.COMPLETED or status == RecognitionStatus.FAILED:
            result = await RecognitionEntity.get(id)
            if result:
                result.status = status
                await result.save()
    