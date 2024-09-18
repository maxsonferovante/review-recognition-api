
from nest.core import Injectable
from .config import config, version

@Injectable
class AppService:
    def __init__(self):
        self.app_name = "Pynest App"
        self.app_version = version

    def get_app_info(self):
        return {"app_name": self.app_name, "app_version": self.app_version}

