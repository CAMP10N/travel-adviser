from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class BagDimensions:
    width: float
    height: float
    length: float
    weight: float


@dataclass
class BagPolicy:
    hand_bag_dimensions: BagDimensions
    hold_bag_dimensions: BagDimensions
    personal_item_dimensions: BagDimensions | None


@dataclass
class Fare:
    adults: float
    children: float
    infants: float


@dataclass
class FlightSchedule:
    departure_local: datetime
    departure_utc: datetime
    arrival_local: datetime
    arrival_utc: datetime


@dataclass
class SinglePossibleOrder:
    bag_policy: BagPolicy
    duration: float
    distance: float
    price: Fare
    bag_price: float
    availability: int
    flight_dates: FlightSchedule
    airline: str


@dataclass
class FlightsResponse:
    options: List[SinglePossibleOrder]
