from nest.core import PyNestFactory, Module
from .config import config, version
from .app_controller import AppController
from .app_service import AppService
from src.modules.recognition.recognition_module import RecognitionModule
from src.modules.review.review_module import ReviewModule


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


@http_server.on_event("startup")
async def startup():
    await config.create_all()
