from nest.core import Module
from .recognition_controller import RecognitionController
from .recognition_service import RecognitionService


@Module(
    controllers=[RecognitionController],
    providers=[RecognitionService],
    imports=[]
)   
class RecognitionModule:
    pass

    