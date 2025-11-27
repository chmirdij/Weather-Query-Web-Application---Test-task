import pytest
import json
import asyncio

from sqlalchemy import insert

from app.config import settings
from app.database import engine, Base, async_session_maker
from app.logger import logger
from app.weather_queries.models import WeatherQueries


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Test db has been created")

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", "r", encoding="utf-8") as f:
            return json.load(f)

    weather_queries = open_mock_json("weather_queries")

    async with async_session_maker() as session:
        query = insert(WeatherQueries).values(weather_queries)
        await session.execute(query)
        await session.commit()
        logger.info("Test data has been inserted into database")


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

