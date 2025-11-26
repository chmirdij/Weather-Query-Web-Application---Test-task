from fastapi import FastAPI

from app.middleware.rate_limiter import RateLimiterMiddleware
from app.redis_client import redis_client
from app.weather_queries.router import router as weather_router
from app.health.router import router as health_router


app = FastAPI()

app.add_middleware(RateLimiterMiddleware, redis_client=redis_client)

app.include_router(weather_router)
app.include_router(health_router)