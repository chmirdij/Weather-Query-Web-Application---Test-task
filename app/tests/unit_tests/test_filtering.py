from datetime import datetime, timezone
import pytest

from app.weather_queries.service import WeatherService


@pytest.mark.parametrize("city,date_from,date_to,total", [
    ("Minsk", "2025-11-25", "2025-12-25", 20),
    ("Minsk", "2024-11-25", "2024-12-25", 20),
    ("Moscow", "2025-11-25", "2025-12-25", 30),
])
async def test_filtering(city, date_from, date_to, total):
    date_from = datetime.strptime(date_from, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    result = await WeatherService.get_all_queries(city=city)

    assert result["total"] == total

    for item in result["items"]:
        assert city in item["city"]

    result = await WeatherService.get_all_queries(date_from=date_from)
    assert all(item["timestamp"] >= date_from for item in result["items"])