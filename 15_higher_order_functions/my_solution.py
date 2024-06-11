from typing import Any, Protocol
from functools import partial

import requests
import os
import dotenv

dotenv.load_dotenv()

API_KEY = os.getenv("API_KEY")


class CityNotFoundError(Exception):
    pass

def get_forecast_http(url: str) -> dict[str, Any]:
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # Raise an exception if the request failed
    return response.json()


def retrieve_forecast(http_fn: callable, city: str, api_key: str) -> None:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = http_fn(url)
    if "main" not in response:
        raise CityNotFoundError(
            f"Couldn't find weather data. Check '{city}' if it exists and is correctly spelled.\n"
        )
    return response


def temperature(forecast_obj: dict) -> float:
    return forecast_obj["main"]["temp"] - 273.15


def humidity(forecast_obj: dict) -> int:
    return forecast_obj["main"]["humidity"]


def wind_speed(forecast_obj: dict) -> float:
    return forecast_obj["wind"]["speed"]


def wind_direction(forecast_obj: dict) -> int:
    return forecast_obj["wind"]["deg"]


def main() -> None:
    city = "Utrecht"

    my_retrieve_forecast = partial(retrieve_forecast, http_fn=get_forecast_http, api_key=API_KEY)
    response = my_retrieve_forecast(city=city)
    print(f"The current temperature in {city} is {temperature(response):.1f} °C.")
    print(f"The current humidity in {city} is {humidity(response)}%.")
    print(
        f"The current wind speed in {city} is {wind_speed(response)} m/s from direction {wind_direction(response)} degrees."
    )


if __name__ == "__main__":
    main()
