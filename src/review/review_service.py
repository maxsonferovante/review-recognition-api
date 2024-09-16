from .review_model import Review
from .review_entity import Review as ReviewEntity
from nest.core.decorators.database import db_request_handler
from nest.core import Injectable


@Injectable
class ReviewService:

    @db_request_handler
    async def add_review(self, review: Review):
        new_review = ReviewEntity(
            **review.dict()
        )
        await new_review.save()
        return new_review.id

    @db_request_handler
    async def get_review(self):
        return await ReviewEntity.find_all().to_list()
