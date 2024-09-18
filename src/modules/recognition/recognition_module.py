from nest.core import Module
from .recognition_controller import RecognitionController
from .recognition_service import RecognitionService
from src.modules.character_recognition.character_recognition_module import CharacterRecognitionModule

@Module(
    controllers=[RecognitionController],
    providers=[RecognitionService],
    imports=[CharacterRecognitionModule]
)   
class RecognitionModule:
    pass

    