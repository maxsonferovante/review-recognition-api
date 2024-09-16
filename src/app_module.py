from nest.core import PyNestFactory, Module
from .config import config
from .app_controller import AppController
from .app_service import AppService
from src.recognition.recognition_module import RecognitionModule
from src.review.review_module import ReviewModule


@Module(
    imports=[RecognitionModule, ReviewModule],
    controllers=[AppController],
    providers=[AppService],
)
class AppModule:
    pass


app = PyNestFactory.create(
    AppModule,
    description="This is my Async PyNest app.",
    title="PyNest Application",
    version="1.0.0",
    debug=True,
    docs_url="/api/docs"
)
http_server = app.get_server()


@http_server.on_event("startup")
async def startup():
    await config.create_all()
