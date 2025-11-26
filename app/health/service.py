from app.config import settings
from app.database import async_session_maker

from sqlalchemy import text
import requests


class HealthService:
    @staticmethod
    async def check_db_connection():
        try:
            async with async_session_maker() as session:
                await session.execute(text("SELECT 1"))

            return {"status": "ok"}

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    @staticmethod
    async def check_api_connection():
        try:
            params = {
                "q": "minsk",
                "appid": settings.OW_API_KEY,
            }
            response = requests.get(settings.OW_URL, params=params,timeout=3)
            response.raise_for_status()

            return {"status": "ok"}

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }
