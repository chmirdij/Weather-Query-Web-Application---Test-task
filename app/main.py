from http.client import HTTPException

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.exceptions import AppException
from app.middleware.rate_limiter import RateLimiterMiddleware
from app.middleware.logging import LoggingMiddleware
from app.redis_client import redis_client
from app.weather_queries.router import router as weather_router
from app.health.router import router as health_router


app = FastAPI()

app.add_middleware(RateLimiterMiddleware, redis_client=redis_client)
app.add_middleware(LoggingMiddleware)

app.add_exception_handler(Exception, AppException.exception_handler)
app.add_exception_handler(HTTPException, AppException.http_exception_handler)
app.add_exception_handler(RequestValidationError, AppException.validation_exception_handler)

app.include_router(weather_router)
app.include_router(health_router)