from nest.core import Controller, Get, Post

from .review_service import ReviewService
from .review_model import Review


@Controller("review")
class ReviewController:

    def __init__(self, review_service: ReviewService):
        self.service = service

    @Get("/")
    async def get_review(self):
        return await self.review_service.get_review()

    @Post("/")
    async def add_review(self, review: Review):
        return await self.review_service.add_review(review)
 