from dataclasses import dataclass
from enum import Enum, auto
from typing import List


class ForecastType(Enum):
    Prediction = auto()
    Historic = auto()
    Error = auto()


@dataclass
class SingleWeatherResponse:
    day: int
    month: int
    temperature: float
    feels_like: float
    humidity: float
    description: str
    wind_speed: float


@dataclass
class ForecastResponse:
    daily_forecast: List[SingleWeatherResponse]
    type_of_forecast: ForecastType
    average_temp: float
    min_temp: float
    max_temp: float
    average_feels_like: float
    min_feels_like: float
    max_feels_like: float
    average_humidity: float
    min_humidity: float
    max_humidity: float
    average_wind_speed: float
    min_wind_speed: float
    max_wind_speed: float
    mode_description: str


BadForecastResponse = ForecastResponse(
    [],
    ForecastType.Error,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "")
