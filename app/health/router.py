from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.health.service import HealthService

router = APIRouter(
    prefix="/health",
    tags=["Basic health check"],
)

@router.get("/db")
async def db_health_check():
    db_check = await HealthService.check_db_connection()

    if db_check["status"] != "ok":
        http_status = status.HTTP_503_SERVICE_UNAVAILABLE
    else:
        http_status = status.HTTP_200_OK

    return JSONResponse(
        status_code=http_status,
        content=db_check,
    )

@router.get("/ow_api")
async def api_health_check():
    api_check = await HealthService.check_api_connection()

    if api_check["status"] != "ok":
        http_status = status.HTTP_503_SERVICE_UNAVAILABLE
    else:
        http_status = status.HTTP_200_OK

    return JSONResponse(
        status_code=http_status,
        content=api_check,
    )

