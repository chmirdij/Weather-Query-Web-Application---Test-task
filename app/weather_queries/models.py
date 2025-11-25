from sqlalchemy import Column, Identity, Integer, String, Boolean, DateTime, JSON, Float
from sqlalchemy.sql import func

from app.database import Base


class WeatherQueries(Base):
    __tablename__ = 'weather_queries'

    id = Column(Integer, Identity(increment=1, start=1), primary_key=True)
    city = Column(String, index=True)
    unit = Column(String, default='metric')
    temperature = Column(Float)
    description = Column(String)
    served_from_cache = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    weather_data = Column(JSON)