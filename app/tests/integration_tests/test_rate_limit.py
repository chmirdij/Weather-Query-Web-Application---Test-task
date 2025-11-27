from app.main import app as fastapi_app
from app.weather_queries.service import WeatherService


async def test_rate_limit(
        monkeypatch,
        async_client,
        fake_redis_client,
        override_rate_limiter_redis_middleware
):
    override_rate_limiter_redis_middleware(fastapi_app, fake_redis_client)

    queries_amount_before = await WeatherService.get_queries_amount()

    response = await async_client.get("/weather?city=Minsk")

    queries_amount_after = await WeatherService.get_queries_amount()

    assert queries_amount_before == queries_amount_after
    assert response.status_code == 429
    assert response.json()["detail"] == "Too many requests, please try again later."
