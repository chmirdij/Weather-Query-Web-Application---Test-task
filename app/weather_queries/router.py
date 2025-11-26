from typing import Literal
from datetime import datetime
import csv

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from app.weather_queries.service import WeatherService

router = APIRouter(
    prefix="/weather",
    tags=["Weather queries"]
)

@router.get("")
async def get_weather_by_city(
        city: str = Query(...),
        unit: Literal["metric", "imperial", "standard"] = Query("metric", description="metric = Celsius, imperial = Fahrenheit, standard = Kelvin")
):
    parsed, served_from_cache = await WeatherService.get_weather_data_with_cache(city, unit)
    return {**dict(parsed), "served_from_cache": served_from_cache, "unit": unit}


@router.get("/queries")
async def get_all_queries(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
        city: str | None = Query(None),
        date_from: datetime | None = Query(None, description="Filter from date, format: YYYY-MM-DD"),
        date_to: datetime | None = Query(None, description="Filter to date, format: YYYY-MM-DD"),
):
    # print("DEBUG-----", date_from.timestamp())
    result = await WeatherService.get_all_queries(page, limit, city, date_from, date_to)
    return result

@router.get("/queries/export")
async def export_queries(
city: str | None = Query(None),
        date_from: datetime | None = Query(None, description="Filter from date, format: YYYY-MM-DD"),
        date_to: datetime | None = Query(None, description="Filter to date, format: YYYY-MM-DD"),
):
    data = await WeatherService.get_queries_for_export(city, date_from, date_to)

    def iter_csv():
        writer = csv.writer
        yield ",".join(["city", "unit", "temperature", "description", "timestamp", "served_from_cache"]) + "\n"
        for row in data:
            yield ",".join([
                str(row["city"]),
                str(row["unit"]),
                str(row["temperature"]),
                str(row["description"]),
                row["timestamp"].isoformat(),
                str(row["served_from_cache"])
            ]) + "\n"

    return StreamingResponse(
        iter_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="queries.csv"'}
    )