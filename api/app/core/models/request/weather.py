from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel


class WeatherRequest(BaseModel):
    city: str
    country: str
    start_day: int
    start_month: int
    start_year: int
    end_day: int
    end_month: int
    end_year: int


@dataclass
class Coordinates:
    longitude: float
    latitude: float


@dataclass
class Dates:
    start: datetime
    end: datetime
