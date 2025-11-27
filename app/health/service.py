from app.database import async_session_maker

from sqlalchemy import text

from app.logger import logger
from app.weather_queries.service import WeatherService


class HealthService:
    @staticmethod
    async def check_db_connection():
        try:
            async with async_session_maker() as session:
                await session.execute(text("SELECT 1"))

            return {"status": "ok"}

        except Exception as e:
            logger.error("DB connection error", extra={"details": str(e)})
            return {
                "status": "error",
                "message": str(e),
            }

    @staticmethod
    async def check_api_connection():
        try:
            await WeatherService.fetch_weather_data("minsk")

            return {"status": "ok"}

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }
