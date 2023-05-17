from dataclasses import dataclass

from app.core.interactors.weather import IWeatherInteractor
from app.core.models.request.weather import WeatherRequest
from app.core.models.response.core_response import CoreResponse
from app.core.models.response.weather import ForecastResponse


@dataclass
class TravelAdviserCore:
    weather_interactor: IWeatherInteractor

    # coordinates_provider:
    def get_weather_forecast(
        self, request: WeatherRequest
    ) -> CoreResponse[ForecastResponse]:
        return self.weather_interactor.get_weather_forecast(request)
        # if 1 and 0:
        #   return self.weather_interactor.get_daily_forecast(city, country)
        # return self.weather_interactor.get_historic_review(city, country)
