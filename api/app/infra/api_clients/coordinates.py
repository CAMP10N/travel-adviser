import json
from typing import Protocol

import requests

from app.core.models.request.weather import Coordinates


class ICoordinateProvider(Protocol):
    def get_coordinates(self, city: str, country: str) -> Coordinates:
        pass


class DefaultCoordinateProvider:
    request_url: str = "https://api.openweathermap.org/geo/1.0/direct"
    api_key: str = "6a03a52969e6134ed33eccf7d2bffac8"

    def get_coordinates(self, city: str, country: str) -> Coordinates:
        params = {"q": city, "appid": self.api_key}
        response = requests.get(self.request_url, params=params)
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    # Assuming the response is an array of objects
                    if data:  # Check if the array is not empty
                        first_object = data[0]
                        lat = first_object["lat"]
                        lon = first_object["lon"]
                        print(type(lon))
                        return Coordinates(lon, lat)
                else:
                    print("Invalid response format: Expected an array of objects")
            except json.JSONDecodeError as e:
                print("Error parsing JSON:", str(e))
                return Coordinates(0, 0)
        # Request was not successful
        print("Request failed with status code:", response.status_code)
        return Coordinates(0, 0)
