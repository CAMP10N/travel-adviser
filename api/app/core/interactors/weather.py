from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from app.core.models.request.weather import Dates, WeatherRequest
from app.core.models.response.core_response import CoreResponse, CoreStatus
from app.core.models.response.weather import ForecastResponse, ForecastType
from app.core.utils.forecast_type_strategy import IForecastTypeStrategy
from app.infra.api_clients.coordinates import ICoordinateProvider
from app.infra.api_clients.weather import IWeatherProvider


class IWeatherInteractor(Protocol):
    def get_weather_forecast(
        self, request: WeatherRequest
    ) -> CoreResponse[ForecastResponse]:
        pass


@dataclass
class WeatherInteractor:
    coordinates_provider: ICoordinateProvider
    forecast_provider: IWeatherProvider
    forecast_type_strategy: IForecastTypeStrategy

    def get_weather_forecast(
        self, request: WeatherRequest
    ) -> CoreResponse[ForecastResponse]:
        start_date = datetime(
            request.start_year, request.start_month, request.start_day
        )
        end_date = datetime(request.end_year, request.end_month, request.end_day)
        type_of_forecast = self.forecast_type_strategy.choose_type(start_date, end_date)
        coordinates = self.coordinates_provider.get_coordinates(
            request.city, request.country
        )
        dates = Dates(start_date, end_date)
        response_content: ForecastResponse
        if type_of_forecast == ForecastType.Prediction:
            response_content = self.forecast_provider.get_forecast(coordinates, dates)
        else:
            response_content = self.forecast_provider.get_historic_data(
                coordinates, dates
            )
        response: CoreResponse[ForecastResponse] = CoreResponse(None)
        response.response_content = response_content
        response.status = CoreStatus.SUCCESSFUL_GET
        response.message = "Success"
        return response
