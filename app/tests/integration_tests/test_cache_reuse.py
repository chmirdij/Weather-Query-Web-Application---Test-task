from app.weather_queries.service import WeatherService


async def test_cache_reuse(
        monkeypatch,
        fake_redis_client,
        fake_fetch_weather_data,
        fake_add_weather_data
):
    monkeypatch.setattr("app.weather_queries.service.redis_client", fake_redis_client)
    monkeypatch.setattr(WeatherService, "fetch_weather_data", fake_fetch_weather_data)
    monkeypatch.setattr(WeatherService, "add_weather_data", fake_add_weather_data)

    _, cache_ = await WeatherService.get_weather_data_with_cache("Minsk")
    assert cache_ is False
    assert fake_fetch_weather_data.calls["count"] == 1

    _, cache_ = await WeatherService.get_weather_data_with_cache("Minsk")
    assert cache_ is True
    assert fake_fetch_weather_data.calls["count"] == 1

    _, cache_ = await WeatherService.get_weather_data_with_cache("Moscow")
    assert cache_ is False
    assert fake_fetch_weather_data.calls["count"] == 2

    _, cache_ = await WeatherService.get_weather_data_with_cache("Minsk")
    assert cache_ is True
    assert fake_fetch_weather_data.calls["count"] == 2

