import json
from dataclasses import field
from datetime import datetime, timedelta
from typing import Callable, Dict, List, Protocol, Tuple

import requests
from dateutil.relativedelta import relativedelta

from app.core.models.request.weather import Coordinates, Dates
from app.core.models.response.weather import (
    ForecastResponse,
    ForecastType,
    SingleWeatherResponse, BadForecastResponse,
)


class IWeatherProvider(Protocol):
    def get_forecast(self, coordinates: Coordinates, dates: Dates) -> ForecastResponse:
        pass

    def get_historic_data(
        self, coordinates: Coordinates, dates: Dates
    ) -> ForecastResponse:
        pass


def default_aggregator(
    data: List[SingleWeatherResponse], forecast_type: ForecastType
) -> ForecastResponse:
    avg_temp: float = 0
    min_temp: float = 100000
    max_temp: float = -100000
    avg_feels_like: float = 0
    min_feels_like: float = 100000
    max_feels_like: float = -100000
    avg_humidity: float = 0
    min_humidity: float = 100000
    max_humidity: float = -100000
    avg_wind_speed: float = 0
    min_wind_speed: float = 100000
    max_wind_speed: float = -100000
    descr: Dict[str, int] = {}
    count: int = 0
    for forecast in data:
        avg_temp += forecast.temperature
        min_temp = min(min_temp, forecast.temperature)
        max_temp = max(max_temp, forecast.temperature)
        avg_feels_like += forecast.feels_like
        min_feels_like = min(min_feels_like, forecast.feels_like)
        max_feels_like = max(max_feels_like, forecast.feels_like)
        avg_humidity += forecast.humidity
        min_humidity = min(min_humidity, forecast.humidity)
        max_humidity = max(max_humidity, forecast.humidity)
        avg_wind_speed += forecast.wind_speed
        min_wind_speed = min(min_wind_speed, forecast.wind_speed)
        max_wind_speed = max(max_wind_speed, forecast.wind_speed)
        freq = descr[forecast.description]
        descr[forecast.description] = freq + 1
        count += 1
    avg_temp = float(avg_temp / count)
    avg_feels_like = float(avg_feels_like / count)
    avg_humidity = float(avg_humidity / count)
    avg_wind_speed = float(avg_wind_speed / count)
    mode_descr: str = max(descr, key=descr.get)
    return ForecastResponse(
        daily_forecast=data,
        type_of_forecast=forecast_type,
        average_temp=avg_temp,
        min_temp=min_temp,
        max_temp=max_temp,
        average_humidity=avg_humidity,
        min_humidity=min_humidity,
        max_humidity=max_humidity,
        average_feels_like=avg_feels_like,
        min_feels_like=min_feels_like,
        max_feels_like=max_feels_like,
        average_wind_speed=avg_wind_speed,
        min_wind_speed=min_wind_speed,
        max_wind_speed=max_wind_speed,
        mode_description=mode_descr,
    )


class DefaultWeatherProvider:
    prediction_url: str = "https://api.openweathermap.org/data/3.0/onecall"
    historic_url: str = "https://api.openweathermap.org/data/3.0/onecall/timemachine"  # ?lat=41.76&lon=44.78&dt=1586433000&appid=6a03a52969e6134ed33eccf7d2bffac8&units=metric"
    api_key: str = "6a03a52969e6134ed33eccf7d2bffac8"
    aggregate_strategy: Callable[
        [List[SingleWeatherResponse], ForecastType], ForecastResponse
    ] = field(default=default_aggregator)

    def get_forecast(self, coordinates: Coordinates, dates: Dates) -> ForecastResponse:
        params = {
            "lat": str(coordinates.latitude),
            "lon": str(coordinates.longitude),
            "appid": self.api_key,
            "units": "metric",
        }
        response = requests.get(self.prediction_url, params=params)
        if response.status_code == 200:
            try:
                data = response.json()
                if data:
                    daily_data = data["daily"]
                    if isinstance(daily_data, list):
                        forecast: List[SingleWeatherResponse] = []
                        for day in daily_data:
                            timestamp = day["dt"]
                            dt = datetime.fromtimestamp(timestamp)
                            if not dates.start <= dt <= dates.end:
                                continue
                            temp = day["temp"]["day"]
                            feels_like = day["feels_like"]["day"]
                            humidity = day["humidity"]
                            description = day["weather"]["description"]
                            wind_speed = day["wind_speed"]
                            forecast.append(
                                SingleWeatherResponse(
                                    dt.day,
                                    dt.month,
                                    temp,
                                    feels_like,
                                    humidity,
                                    description,
                                    wind_speed,
                                )
                            )
                        return self.aggregate_strategy(
                            forecast, ForecastType.Prediction
                        )
                else:
                    print("Invalid response format: Expected an array of " "objects")
            except json.JSONDecodeError as e:
                print("Error parsing JSON:", str(e))
                return BadForecastResponse
        # Request was not successful
        print("Request failed with status code:", response.status_code)
        return BadForecastResponse

    def get_historic_data(
        self, coordinates: Coordinates, dates: Dates
    ) -> ForecastResponse:
        params = {
            "lat": str(coordinates.latitude),
            "lon": str(coordinates.longitude),
            "appid": self.api_key,
            "units": "metric",
        }
        curr_now = dates.start
        curr = datetime(
                curr_now.year - 10, curr_now.month, curr_now.day
        ) + timedelta(hours=15)     # Weather at 3PM
        aggregated_data: List[SingleWeatherResponse] = list()
        while curr_now <= dates.end:
            single_day_historic: List[SingleWeatherResponse] = list()
            for i in range(10):
                spec_params = params
                spec_params["dt"] = str(curr.timestamp())
                response = requests.get(self.historic_url, params=params)
                if response.status_code == 200:
                    try:
                        resp = response.json()
                        if resp:
                            data = resp["data"]
                            if isinstance(data, list):
                                elem = data[0]
                                temp = elem["temp"]
                                feels_like = elem["feels_like"]
                                humidity = elem["humidity"]
                                description = elem["weather"]["description"]
                                wind_speed = elem["wind_speed"]
                                single_day_historic.append(
                                    SingleWeatherResponse(
                                        curr.day,
                                        curr.month,
                                        temp,
                                        feels_like,
                                        humidity,
                                        description,
                                        wind_speed,
                                    )
                                )
                        else:
                            print(
                                "Invalid response format: Expected an array of objects"
                            )
                    except json.JSONDecodeError as e:
                        print("Error parsing JSON:", str(e))
                        return BadForecastResponse
                curr = curr + relativedelta(year=1)
            one_day_aggregated: ForecastResponse = self.aggregate_strategy(
                                                        single_day_historic,
                                                        ForecastType.Historic)
            aggregated_data.append(
                SingleWeatherResponse(
                    one_day_aggregated.daily_forecast[0].day,
                    one_day_aggregated.daily_forecast[0].month,
                    one_day_aggregated.average_temp,
                    one_day_aggregated.average_feels_like,
                    one_day_aggregated.average_humidity,
                    one_day_aggregated.mode_description,
                    one_day_aggregated.average_wind_speed
                )
            )
            curr_now += timedelta(days=1)
            curr = datetime(
                curr_now.year - 10, curr_now.month, curr_now.day
            ) + timedelta(hours=15)
        return self.aggregate_strategy(aggregated_data, ForecastType.Historic)
