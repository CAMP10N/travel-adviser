from datetime import datetime
from enum import Enum
from typing import Tuple, List

from pydantic import BaseModel


class Currency(Enum):
    GEL = "GEL"
    EUR = "EUR"
    USD = "USD"


class TravellingLocation:
    locations: List[str]
    nights_range: Tuple[int, int]
    dates_range: Tuple[str, str] | None


class FlightsRequest(BaseModel):
    adults: int
    children: int = 0
    date_from: datetime
    date_to: datetime
    currency: Currency
    fly_from: str
    fly_to: str
    intermediate_locations: List[TravellingLocation] = []
    return_from: datetime | None
    return_to: datetime | None







