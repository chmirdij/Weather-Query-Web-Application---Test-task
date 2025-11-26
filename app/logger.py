import logging
from pythonjsonlogger.json import JsonFormatter



logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()

formatter = JsonFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)