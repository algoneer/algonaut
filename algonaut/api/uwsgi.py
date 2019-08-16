from algonaut.settings import settings
from .app import get_app


settings.setup_logging(settings.get("loglevel", 4))
settings.initialize()
app = get_app(settings)
