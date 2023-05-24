from fastapi import APIRouter, Depends, Response

from app.core.facade import TravelAdviserCore
from app.core.models.request.flights import FlightsRequest
from app.core.models.response.flights import FlightsResponse
from app.infra.fastAPI.dependables import get_core

weather_api: APIRouter = APIRouter()


@weather_api.get(
    "/flights/"
)
def get_statistics(
    response: Response,
    request: FlightsRequest,
    core: TravelAdviserCore = Depends(get_core),
) -> FlightsResponse:
    core_response = core.get_flights(request)
    return core_response.response_content