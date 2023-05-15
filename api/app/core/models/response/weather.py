from dataclasses import dataclass
from enum import Enum, auto
from typing import List


class ForecastType(Enum):
    Prediction = auto()
    Historic = auto()


@dataclass
class SingleWeatherResponse:
    temperature: float
    feels_like: float
    humidity: float
    description: str
    wind_speed: float


@dataclass
class ForecastResponse:
    daily_forecast: List[SingleWeatherResponse]
    type_of_forecast: ForecastType
    average_temp: float | None
    mode_temp: float | None
    mode_description: str | None
