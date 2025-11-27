import requests
import json
import time
from sqlalchemy import insert, select, func, and_
from datetime import datetime

from app.config import settings
from app.database import async_session_maker
from app.logger import logger
from app.redis_client import redis_client
from app.weather_queries.models import WeatherQueries
from app.weather_queries.schemas import WeatherApiResponse


class WeatherService:
    _model = WeatherQueries

    @classmethod
    async def fetch_weather_data(cls, city: str, units: str = "metric"):
        params = {
            "q": city,
            "units": units,
            "appid": settings.OW_API_KEY,
        }

        start_time = time.perf_counter()

        try:
            response = requests.get(settings.OW_URL, params=params, timeout=5)
            response.raise_for_status()

            duration = time.perf_counter() - start_time
            logger.info("API request", extra={"api_latency": round(duration * 1000, 2)})

            row = response.json()
            parsed = WeatherApiResponse.parse_api_response(row)

            return row, parsed

        except Exception as e:
            logger.error("Api connection error", extra={"details": str(e)})
            raise



    @classmethod
    async def get_weather_data_with_cache(cls, city: str, unit: str = "metric"):
        redis_key = f"weather_cache:{city.lower()}:{unit}"

        try:
            cached_data = await redis_client.get(redis_key)

        except Exception as e:
            logger.error("Redis connection error", extra={"details": str(e)})
            cached_data = None

        if cached_data:
            data = json.loads(cached_data)
            served_from_cache = True
        else:
            row, parsed = await cls.fetch_weather_data(city, unit)
            served_from_cache = False

            data = dict(parsed)
            data["row"] = row

            try:
                await redis_client.setex(redis_key, 300, json.dumps(data))
            except Exception as e:
                logger.error("Redis connection error", extra={"details": str(e)})

        row = data["row"]
        parsed = WeatherApiResponse.parse_api_response(row)
        await cls.add_weather_data(row, parsed, unit, served_from_cache)

        return parsed, served_from_cache



    @classmethod
    async def add_weather_data(cls, row_data, parsed_data, unit: str = "metric", served_from_cache=False):
        async with async_session_maker() as session:
            params = {
                "city": parsed_data.city,
                "unit": unit,
                "served_from_cache": served_from_cache,
                "temperature": parsed_data.temperature,
                "description": parsed_data.description,
                "weather_data": row_data
            }

            query = insert(cls._model).values(params)
            await session.execute(query)
            await session.commit()


    @classmethod
    async def get_all_queries(
            cls,
            page: int,
            limit: int,
            city: str | None = None,
            date_from: datetime | None = None,
            date_to: datetime | None = None,
    ):
        async with async_session_maker() as session:
            filters = []
            if city:
                filters.append(cls._model.city.ilike(f"%{city}%"))
            if date_from:
                filters.append(cls._model.timestamp >= date_from)
            if date_to:
                filters.append(cls._model.timestamp <= date_to)

            total_filter = and_(*filters) if filters else None

            query = (
                select(
                    cls._model.id,
                    cls._model.city,
                    cls._model.unit,
                    cls._model.temperature,
                    cls._model.description,
                    cls._model.timestamp,
                    cls._model.served_from_cache,
                    func.count().over().label("total")
                )
                .offset((page - 1) * limit)
                .limit(limit)
            )

            if total_filter is not None:
                query = query.where(total_filter)

            result = await session.execute(query)
            data = result.mappings().all()

            if not data:
                return {
                    "total": 0,
                    "page": page,
                    "limit": limit,
                    "items": []
                }

            total = data[0]["total"]

            data = [dict(el) for el in data]
            for item in data:
                item.pop("total")

            return {
                "total": total,
                "page": page,
                "limit": limit,
                "items": data
            }

    @classmethod
    async def get_queries_for_export(
            cls,
            city: str | None = None,
            date_from: datetime | None = None,
            date_to: datetime | None = None,
    ):
        async with async_session_maker() as session:
            filters = []
            if city:
                filters.append(cls._model.city.ilike(f"%{city}%"))
            if date_from:
                filters.append(cls._model.timestamp >= date_from)
            if date_to:
                filters.append(cls._model.timestamp <= date_to)

            total_filter = and_(*filters) if filters else None

            query = (
                select(
                    cls._model.id,
                    cls._model.city,
                    cls._model.unit,
                    cls._model.temperature,
                    cls._model.description,
                    cls._model.timestamp,
                    cls._model.served_from_cache,
                    func.count().over().label("total")
                )
            )

            if total_filter is not None:
                query = query.where(total_filter)

            result = await session.execute(query)
            return result.mappings().all()


# r, p = WeatherService.fetch_weather_data(city="London", units="metric")
# dp = dict(p)
# dp["row"] = r
# print(dp)