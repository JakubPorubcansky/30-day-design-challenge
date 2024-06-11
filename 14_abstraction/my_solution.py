from typing import Any, Protocol

import requests
import os
import dotenv

dotenv.load_dotenv()

API_KEY = os.getenv("API_KEY")

class CityNotFoundError(Exception):
    pass

class IRequestsClient(Protocol):
    def get(self, url: str, timeout: int):
        ...

class RequestsClient():
    def get(self, url: str, timeout: int):
        return requests.get(url, timeout=timeout).json()
    

class WeatherService:
    def __init__(self, api_key: str, requests_client: IRequestsClient) -> None:
        self.api_key = api_key
        self.full_weather_forecast: dict[str, Any] = {}
        self.requests_client = requests_client

    def retrieve_forecast(self, city: str) -> None:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}"
        response = self.requests_client.get(url, timeout=5)
        if "main" not in response:
            raise CityNotFoundError(
                f"Couldn't find weather data. Check '{city}' if it exists and is correctly spelled.\n"
            )
        self.full_weather_forecast = response


def main() -> None:
    city = "Utrecht"
    rc = RequestsClient()
    client = WeatherService(api_key=API_KEY, requests_client=rc)
    client.retrieve_forecast(city=city)
    temp = client.full_weather_forecast["main"]["temp"] - 273.15
    hum = client.full_weather_forecast["main"]["humidity"]
    wind_speed = client.full_weather_forecast["wind"]["speed"]
    wind_direction = client.full_weather_forecast["wind"]["deg"]
    print(f"The current temperature in {city} is {temp:.1f} °C.")
    print(f"The current humidity in {city} is {hum}%.")
    print(
        f"The current wind speed in {city} is {wind_speed} m/s from direction {wind_direction} degrees."
    )


if __name__ == "__main__":
    main()
