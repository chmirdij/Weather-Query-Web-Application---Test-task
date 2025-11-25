from fastapi import FastAPI

from app.weather_queries.router import router as weather_router

app = FastAPI()

app.include_router(weather_router)