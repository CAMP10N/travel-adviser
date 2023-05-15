from fastapi import FastAPI

from app.infra.fastAPI.endpoints.weather import weather_api


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(weather_api)
    return app
