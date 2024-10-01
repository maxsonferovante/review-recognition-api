from nest.core import PyNestFactory, Module
from .config import config, version
from .app_controller import AppController
from .app_service import AppService
from src.modules.recognition.recognition_module import RecognitionModule
from src.modules.review.review_module import ReviewModule

from src.middlewares.rate_limit_middleware import RateLimitMiddleware
from src.middlewares.recognition_validation_middleware import RecognitionValidationMiddleware
@Module(
    imports=[RecognitionModule, ReviewModule],
    controllers=[AppController],
    providers=[AppService],
)
class AppModule:
    pass


app = PyNestFactory.create(
    AppModule,
    description="The Review Recognition API is an application that allows the analysis and extraction of information from reviews in PDF format.",
    title="API Review Recognition",
    version=version,
    debug=True,
    docs_url="/api/docs"
)

http_server = app.get_server()

# Add middleware to the server instance: 
#  - RateLimitMiddleware: Limit the number of requests per client IP.
http_server.add_middleware(RateLimitMiddleware, max_requests=50, window_seconds=60)
#  - RecognitionValidationMiddleware: Validate the file type and size of the uploaded file.
http_server.add_middleware(RecognitionValidationMiddleware)

@http_server.on_event("startup")
async def startup():
    await config.create_all()
