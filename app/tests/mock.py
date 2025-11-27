from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select
import json
import asyncio

from app.config import settings
from app.logger import logger
from app.weather_queries.models import WeatherQueries


async def get_test_data_from_db(model):
    engine = create_async_engine(settings.database_url)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session_maker() as session:
        columns = [col for col in model.__table__.columns if col.name != "id" and col.name != "timestamp"]
        query = select(*columns).limit(50)
        result = await session.execute(query)

        await engine.dispose()

        result = result.mappings().all()

        return [dict(obj) for obj in result]


async def dump_model_to_json(model, model_name: str):
    data = await get_test_data_from_db(model)

    with open(f"app/tests/mock_{model_name}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, default=str, ensure_ascii=False)

    logger.info(f"Mock for {model_name} has been created")

if __name__ == "__main__":
    asyncio.run(dump_model_to_json(WeatherQueries, "weather_queries"))