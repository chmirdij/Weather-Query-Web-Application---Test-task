import pytest

from app.weather_queries.service import WeatherService

@pytest.mark.parametrize("city,page,limit,total", [
    ("Minsk", 1, 10, 20),
    ("Minsk", 2, 10, 20),
    ("Minsk", 1, 20, 20),
])
async def test_pagination(city, page, limit, total):
    result = await WeatherService.get_all_queries(page, limit, city=city)

    assert result["total"] == total
    assert len(result["items"]) == limit
