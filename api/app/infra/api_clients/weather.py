import json
from datetime import datetime, timedelta
from typing import List, Protocol, Tuple, Dict

import requests

from app.core.models.request.weather import Coordinates, Dates
from app.core.models.response.weather import (
    ForecastResponse,
    ForecastType,
    SingleWeatherResponse,
)


class IWeatherProvider(Protocol):
    def get_forecast(self, coordinates: Coordinates, dates: Dates) -> ForecastResponse:
        pass

    def get_historic_data(
        self, coordinates: Coordinates, dates: Dates
    ) -> ForecastResponse:
        pass


class DefaultWeatherProvider:
    prediction_url: str = "https://api.openweathermap.org/data/3.0/onecall"
    historic_url: str = "https://api.openweathermap.org/data/3.0/onecall/timemachine" # ?lat=41.76&lon=44.78&dt=1586433000&appid=6a03a52969e6134ed33eccf7d2bffac8&units=metric"
    api_key: str = "6a03a52969e6134ed33eccf7d2bffac8"

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
                            # TODO check if dt is in Dates range
                            temp = day["temp"]["day"]
                            feels_like = day["feels_like"]["day"]
                            humidity = day["humidity"]
                            description = day["weather"]["description"]
                            wind_speed = day["wind_speed"]
                            forecast.append(
                                SingleWeatherResponse(
                                    temp, feels_like, humidity, description, wind_speed
                                )
                            )
                        return ForecastResponse(
                            daily_forecast=forecast,
                            type_of_forecast=ForecastType.Prediction,
                            average_temp=None,
                            mode_temp=None,
                            mode_description=None,
                        )
                else:
                    print("Invalid response format: Expected an array of objects")
            except json.JSONDecodeError as e:
                print("Error parsing JSON:", str(e))
                return ForecastResponse(
                    daily_forecast=[],
                    type_of_forecast=ForecastType.Prediction,
                    average_temp=None,
                    mode_temp=None,
                    mode_description=None,
                )
        # Request was not successful
        print("Request failed with status code:", response.status_code)
        return ForecastResponse(
            daily_forecast=[],
            type_of_forecast=ForecastType.Prediction,
            average_temp=None,
            mode_temp=None,
            mode_description=None,
        )

    def get_historic_data(
        self, coordinates: Coordinates, dates: Dates
    ) -> ForecastResponse:
        params = {
            "lat": str(coordinates.latitude),
            "lon": str(coordinates.longitude),
            "appid": self.api_key,
            "units": "metric",
        }
        rame: Dict[Tuple[int, int], List[SingleWeatherResponse]] = dict()

        for i in range(10):
            start_date = datetime(dates.start.year-i-1, dates.start.month, dates.start.day)
            start_date = start_date + timedelta(hours=15)
            end_date = datetime(dates.start.year-i-1, dates.start.month, dates.start.day)
            end_date = end_date + timedelta(hours=15)
            curr = start_date
            while curr <= end_date:
                spec_params = params
                spec_params["dt"] = start_date
                response = requests.get(self.historic_url, params=params)
                curr_list = rame[(curr.month, curr.day)]
                if response.status_code == 200:
                    try:
                        resp = response.json()
                        if resp:
                            data = resp["data"]
                            if isinstance(data, list):
                                elem = data[0]
                                temp = elem["temp"]
                                feels_like = elem["feels_like"]
                                humidity =elem["humidity"]
                                description = elem["weather"]["description"]
                                wind_speed = elem["wind_speed"]
                                curr_list.append(
                                        SingleWeatherResponse(
                                            temp, feels_like, humidity,
                                            description,
                                            wind_speed
                                        )
                                )

                        else:
                            print(
                                "Invalid response format: Expected an array of objects")
                    except json.JSONDecodeError as e:
                        print("Error parsing JSON:", str(e))
                        return ForecastResponse(
                            daily_forecast=[],
                            type_of_forecast=ForecastType.Prediction,
                            average_temp=None,
                            mode_temp=None,
                            mode_description=None,
                        )
                rame[(curr.month, curr.day)] = curr_list
                curr = curr + timedelta(days=1)
            # TODO extra processing

