import pytest
import json
import asyncio

from httpx import AsyncClient, ASGITransport
from sqlalchemy import insert

from app.config import settings
from app.database import engine, Base, async_session_maker
from app.logger import logger
from app.main import app as fastapi_app
from app.middleware.rate_limiter import RateLimiterMiddleware
from app.weather_queries.models import WeatherQueries


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        # logger.info("Test db has been created")

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", "r", encoding="utf-8") as f:
            return json.load(f)

    weather_queries = open_mock_json("weather_queries")

    async with async_session_maker() as session:
        query = insert(WeatherQueries).values(weather_queries)
        await session.execute(query)
        await session.commit()
        # logger.info("Test data has been inserted into database")


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def async_client():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def fake_redis_client():
    class FakeRedis:
        def __init__(self):
            self.store = {}

        async def get(self, key):
            return self.store.get(key)

        async def setex(self, key, ct, value):
            self.store[key] = value

        async def incr(self, key):
            return 999

        async def expire(self, *args, **kwargs):
            pass

    return FakeRedis()

@pytest.fixture()
def override_rate_limiter_redis_middleware():
    def override(app, fake_redis):
        for middleware in app.user_middleware:
            if middleware.cls.__name__ == "RateLimiterMiddleware":
                middleware.kwargs["redis_client"] = fake_redis

    return override

@pytest.fixture()
def fake_fetch_weather_data():
    calls = {"count": 0}

    async def fetch_weather_data(city, unit="metric"):
        calls["count"] += 1
        row = {"coord": {"lon": 37.6156, "lat": 55.7522}, "weather": [{"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04n"}], "base": "stations", "main": {"temp": 1.38, "feels_like": -1.81, "temp_min": 1.24, "temp_max": 1.48, "pressure": 1017, "humidity": 66, "sea_level": 1017, "grnd_level": 997}, "visibility": 8704, "wind": {"speed": 2.96, "deg": 192, "gust": 8.51}, "clouds": {"all": 100}, "dt": 1764082476, "sys": {"type": 2, "id": 2094500, "country": "RU", "sunrise": 1764048271, "sunset": 1764076134}, "timezone": 10800, "id": 524901, "name": "Moscow", "cod": 200}
        parsed = {
            "city": city,
            "temperature": 2.0,
            "description": ""
        }

        return row, parsed

    fetch_weather_data.calls = calls
    return fetch_weather_data

@pytest.fixture()
def fake_add_weather_data():
    async def add_weather_data(row, parsed, unit, served_from_cache):
        return
    return add_weather_data
