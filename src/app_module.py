from nest.core import PyNestFactory, Module
from .config import config, version
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
    description="A API Review Recognition é uma aplicação que permite a análise e extração de informações de reviews de fichas em formato PDF.",
    title="API Review Recognition",
    version=version,
    debug=True,
    docs_url="/api/docs"
)
http_server = app.get_server()


@http_server.on_event("startup")
async def startup():
    await config.create_all()
