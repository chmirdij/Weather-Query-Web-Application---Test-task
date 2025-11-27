import logging
from pythonjsonlogger.json import JsonFormatter

from app.config import settings

logger = logging.getLogger("app")
logger.setLevel(settings.LOG_LEVEL)

handler = logging.StreamHandler()

formatter = JsonFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)