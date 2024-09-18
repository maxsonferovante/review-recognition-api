from nest.core import Module
from .extraction_service import ExtractionService
from .transformation_service import TransformationService
from .character_recognition_service import CharacterRecognitionService

@Module(
    providers=[ExtractionService, TransformationService, CharacterRecognitionService]
)
class CharacterRecognitionModule:
    pass
        