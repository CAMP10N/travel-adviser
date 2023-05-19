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
    average_temp: float | None
    min_temp: float | None
    max_temp: float | None
    average_feels_like: float | None
    min_feels_like: float | None
    max_feels_like: float | None
    average_humidity: float | None
    min_humidity: float | None
    max_humidity: float | None
    average_wind_speed: float | None
    min_wind_speed: float | None
    max_wind_speed: float | None
    mode_description: str | None


BadForecastResponse = ForecastResponse(
    [],
    ForecastType.Error,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
)
