import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from app.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        logger.info(
            "Request started",
            extra={
                "method": request.method,
                "path": request.url.path,
                "client": request.client if request.client else None,
            }
        )

        response = await call_next(request)
        duration = time.perf_counter() - start_time

        logger.info(
            "Request finished",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration": round(duration * 1000, 2)
            }
        )

        return response