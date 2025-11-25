from fastapi import APIRouter, Query

from app.weather_queries.service import WeatherService

router = APIRouter(
    prefix="/weather",
    tags=["Weather queries"]
)

@router.get("")
async def get_weather_by_city(city: str = Query(...), unit: str = Query("metric")):
    row, parsed = WeatherService.fetch_weather_data(city, unit)
    await WeatherService.add_weather_data(row, parsed, unit)
    return parsed