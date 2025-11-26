from pydantic import BaseModel, computed_field
from typing import Any


class WeatherApiResponse(BaseModel):
    city: str
    temperature: float
    description: str

    @classmethod
    def parse_api_response(cls, response: dict):
        return cls(
            city=response["name"],
            temperature=response["main"]["temp"],
            description=response["weather"][0]["description"]
        )
