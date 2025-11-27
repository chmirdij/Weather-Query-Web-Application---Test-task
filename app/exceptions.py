import traceback

from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.logger import logger


class AppException:
    @staticmethod
    def exception_handler(request: Request, exc: Exception):
        logger.error(
            "Global exception",
            extra={
                "path": request.url.path,
                "method": request.method,
                "error_type": type(exc).__name__,
                "error": str(exc),
                "traceback": traceback.format_exc(),
            },
        )

        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
            }
        )

    @staticmethod
    def http_exception_handler(request: Request, exc: HTTPException):
        logger.warning(
            "http_exception",
            extra={
                "path": request.url.path,
                "method": request.method,
                "status_code": exc.status_code,
                "detail": exc.detail,
            }
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    @staticmethod
    def validation_exception_handler(request, exc: RequestValidationError):
        logger.warning(
            "validation_error",
            extra={
                "path": request.url.path,
                "errors": exc.errors(),
                "body": exc.body,
            }
        )

        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors()}
        )