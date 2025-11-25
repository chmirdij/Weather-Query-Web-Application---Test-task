from fastapi import APIRouter, Query

from app.weather_queries.service import WeatherService

router = APIRouter(
    prefix="/weather",
    tags=["Weather queries"]
)

@router.get("")
async def get_weather_by_city(city: str = Query(...), unit: str = Query("metric")):
    parsed, served_from_cache = await WeatherService.get_weather_data_with_cache(city, unit)
    return {**dict(parsed), "served_from_cache": served_from_cache}