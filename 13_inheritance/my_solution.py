import requests


class CityNotFoundError(Exception):
    pass

class WeatherServiceException(Exception):
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg

class WeatherService:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def retrieve_forecast(self, city: str):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}"
        response = self._send_request(url)

        if int(response["cod"]) >= 400:
            raise WeatherServiceException(code=int(response["cod"]), msg=response["message"])
        
        return response["main"]["temp"]

    def _send_request(self, url: str):
        return requests.get(url, timeout=5).json()
    
class MyWeatherService:
    def __init__(self, weather_service: WeatherService):
        self.weather_service = weather_service

    def retrieve_forecast(self, city: str) -> None:
        try:
            temperature = self.weather_service.retrieve_forecast(city)
        except WeatherServiceException as e:
            if e.code == 404:
                raise CityNotFoundError(f"Couldn't find weather data. Check '{city}' if it exists and is correctly spelled.\n") from e
            else:
                raise

        temperature -= 273.15
        print(f"The current temperature in {city} is {temperature:.1f} °C.")


if __name__ == "__main__":
    ws = WeatherService(api_key="ebf34412b1996ce803258dc3a0f54f67")
    my_ws = MyWeatherService(weather_service=ws)
    my_ws.retrieve_forecast(city="Utrecht")
