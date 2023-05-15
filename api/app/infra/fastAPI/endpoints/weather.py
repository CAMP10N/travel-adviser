from fastapi import APIRouter, Depends, Response

from app.core.facade import TravelAdviserCore
from app.core.models.request.weather import WeatherRequest
from app.core.models.response.weather import ForecastResponse
from app.infra.fastAPI.dependables import get_core

weather_api: APIRouter = APIRouter()


@weather_api.get(
    "/weather/city={city}/country={country}/start_date={"
    "start_date}/end_date={end_date}"
)
def get_statistics(
    response: Response,
    request: WeatherRequest,
    core: TravelAdviserCore = Depends(get_core),
) -> ForecastResponse:
    core_response = core.get_weather_forecast(request)
    return ForecastResponse()

