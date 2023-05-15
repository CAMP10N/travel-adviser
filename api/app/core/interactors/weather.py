from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol, Callable

from app.core.models.request.weather import WeatherRequest, Coordinates, Dates
from app.core.models.response.core_response import CoreResponse, CoreStatus
from app.core.models.response.weather import ForecastResponse, ForecastType
from app.infra.api_clients.coordinates import ICoordinateProvider


class IWeatherInteractor(Protocol):
    def get_weather_forecast(self, request: WeatherRequest) -> CoreResponse[ForecastResponse]:
        pass


class IForecastProvider(Protocol):
    def get_forecast(self, coordinates: Coordinates, dates: Dates) -> ForecastResponse:
        pass

    def get_historic_data(self, coordinates: Coordinates, dates: Dates) -> ForecastResponse:
        pass


def racxa(start: datetime, end: datetime) -> ForecastType:
    if (end-start).days > 8:    # TODO further testing required in edge case of 8
        return ForecastType.Historic
    return ForecastType.Prediction


@dataclass
class WeatherInteractor:
    coordinates_provider: ICoordinateProvider
    forecast_provider: IForecastProvider
    forecast_type_strategy: Callable[[datetime, datetime], ForecastType] = field(
        default=racxa
    )

    def get_weather_forecast(self,  request: WeatherRequest) -> CoreResponse[ForecastResponse]:
        start_date = datetime(request.start_year, request.start_month, request.start_day)
        end_date = datetime(request.end_year, request.end_month, request.end_day)
        type_of_forecast = self.forecast_type_strategy(start_date, end_date)
        coordinates = self.coordinates_provider.get_coordinates(request.city, request.country)
        dates = Dates(start_date, end_date)
        response_content: ForecastResponse
        if type_of_forecast == ForecastType.Prediction:
            response_content = self.forecast_provider.get_forecast(coordinates, dates)
        else:
            response_content = self.forecast_provider.get_forecast(coordinates, dates)
        response: CoreResponse[ForecastResponse] = CoreResponse(None)
        response.response_content = response_content
        response.status = CoreStatus.SUCCESSFUL_GET
        response.message = "Success"
        return response
