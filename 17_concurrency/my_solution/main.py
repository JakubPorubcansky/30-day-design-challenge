from dataclasses import dataclass
from typing import Any
import requests
import asyncio
import time

API_KEY = "ebf34412b1996ce803258dc3a0f54f67"

def http_get_sync(url: str):
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # Raise an exception if the request failed
    return response.json()

async def http_get(url: str):
    return await asyncio.to_thread(http_get_sync, url)

@dataclass
class UrlTemplateClient:
    template: str

    async def get(self, data: dict[str, Any]) -> Any:
        url = self.template.format(**data)
        return await http_get(url)


class CityNotFoundError(Exception):
    pass

CAPITALS = {
    "United States of America": "Washington, D.C.",
    "Australia": "Canberra",
    "Japan": "Tokyo",
    "France": "Paris",
    "Brazil": "Brasília",
}


async def get_capital(country: str) -> str:
    client = UrlTemplateClient(template="https://restcountries.com/v3.1/name/{country}")
    # response = client.get({"country": country}) 
    response = [{"capital": [CAPITALS[country]]}]   # mock API (API not responding)
    await asyncio.sleep(2)

    # The API can return multiple matches, so we just return the capital of the first match
    return response[0]["capital"][0]

async def get_forecast(city: str) -> dict[str, Any]:
    client = UrlTemplateClient(
        template=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    )
    
    response = await client.get({"city": city})
    if "main" not in response:
        raise CityNotFoundError(
            f"Couldn't find weather data. Check '{city}' if it exists and is correctly spelled.\n"
        )
    return response


def get_temperature(full_weather_forecast: dict[str, Any]) -> float:
    temperature = full_weather_forecast["main"]["temp"]
    return temperature - 273.15  # convert from Kelvin to Celsius


async def print_temperature_for_capital(country: str) -> None:
    capital = await get_capital(country)
    print(f"The capital of {country} is {capital}")

    weather_forecast = await get_forecast(capital)
    print(f"The current temperature in {capital} is {get_temperature(weather_forecast):.1f} °C.")


async def main() -> None:
    t = time.perf_counter()

    countries = ["United States of America", "Australia", "Japan", "France", "Brazil"]
    await asyncio.gather(*[print_temperature_for_capital(country) for country in countries])

    print("All done!")

    elapsed_time = time.perf_counter() - t
    print(f"Execution time: {elapsed_time:.2f} seconds.")


if __name__ == "__main__":
    asyncio.run(main())
