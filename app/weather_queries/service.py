import requests
from sqlalchemy import insert

from app.config import settings
from app.database import async_session_maker
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
    async def add_weather_data(cls, row_data, parsed_data, unit: str = "metric"):
        async with async_session_maker() as session:
            params = {
                "city": parsed_data.city,
                "unit": unit,
                "served_from_cache": False,
                "temperature": parsed_data.temperature,
                "description": parsed_data.description,
                "weather_data": row_data
            }

            query = insert(cls._model).values(params)
            await session.execute(query)
            await session.commit()

# d = WeatherService.fetch_weather_data(city="London", units="metric")
# p = WeatherApiResponse.parse_api_response(d)
# print(p)