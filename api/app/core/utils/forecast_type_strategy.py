from datetime import datetime
from typing import Protocol

from app.core.models.response.weather import ForecastType


class IForecastTypeStrategy(Protocol):
    def choose_type(self, start: datetime, end: datetime) -> ForecastType:
        pass


class DayCounterStrategy:
    days: int

    def choose_type(self, start: datetime, end: datetime) -> ForecastType:
        if (end - start).days > self.days:
            return ForecastType.Historic
        return ForecastType.Prediction
