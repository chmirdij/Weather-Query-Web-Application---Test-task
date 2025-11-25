import requests
import json
from sqlalchemy import insert

from app.config import settings
from app.database import async_session_maker
from app.redis_client import redis_client
from app.weather_queries.models import WeatherQueries
from app.weather_queries.schemas import WeatherApiResponse


class WeatherService:
    _model = WeatherQueries

    @classmethod
    def fetch_weather_data(cls, city: str, units: str = "metric"):
        params = {
            "q": city,
            "units": units,
            "appid": settings.OW_API_KEY,
        }

        response = requests.get(settings.OW_URL, params=params, timeout=5)
        response.raise_for_status()

        row = response.json()
        parsed = WeatherApiResponse.parse_api_response(row)

        return row, parsed

    @classmethod
    async def get_weather_data_with_cache(cls, city: str, unit: str = "metric"):
        redis_key = f"weather_cache:{city.lower()}:{unit}"

        cached_data = redis_client.get(redis_key)
        if cached_data:
            data = json.loads(cached_data)
            served_from_cache = True
        else:
            row, parsed = cls.fetch_weather_data(city, unit)
            served_from_cache = False

            data = dict(parsed)
            data["row"] = row

            redis_client.setex(redis_key, 300, json.dumps(data))

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

# r, p = WeatherService.fetch_weather_data(city="London", units="metric")
# dp = dict(p)
# dp["row"] = r
# print(dp)