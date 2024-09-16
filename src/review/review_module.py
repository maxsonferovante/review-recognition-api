from nest.core import Module
from .review_controller import ReviewController
from .review_service import ReviewService


@Module(
    controllers=[ReviewController],
    providers=[ReviewService],
    imports=[]
)   
class ReviewModule:
    pass

    