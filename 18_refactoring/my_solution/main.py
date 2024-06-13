from typing import Any, Callable
from enum import Enum
import argparse
from weather import (
    get_complete_forecast,
    http_get,
    get_temperature,
    get_humidity,
    get_wind_speed,
    get_wind_direction,
    get_city_name,
)

class ConditionArgs(Enum):
    TEMPERATURE = ("temperature", "t")
    HUMIDITY = ("humidity", "h")
    WIND = ("wind", "w")
    ALL = ("all", "a")

DEFAULT_CONDITION_ARGS = [ConditionArgs.TEMPERATURE.value[0]]

WeatherProcessingFn = Callable[[dict[str, Any]], None]

def process_temperature(weather_forecast: dict[str, Any]) -> None:
    temperature = get_temperature(weather_forecast)
    print(f"The current temperature in {get_city_name(weather_forecast)} is {temperature:.1f} °C.")

def process_humidity(weather_forecast: dict[str, Any]) -> None:
    print(f"The current humidity in {get_city_name(weather_forecast)} is {get_humidity(weather_forecast)}%.")

def process_wind(weather_forecast: dict[str, Any]) -> None:
    print(
        f"The current wind speed in {get_city_name(weather_forecast)} is {get_wind_speed(weather_forecast)} m/s "
        f"from direction {get_wind_direction(weather_forecast)} degrees."
    )

def map_condition_arg_to_weather_processing_funcs(condition_arg: str) -> list[WeatherProcessingFn]:
    if condition_arg in ConditionArgs.TEMPERATURE.value: return [process_temperature]
    elif condition_arg in ConditionArgs.HUMIDITY.value: return [process_humidity]
    elif condition_arg in ConditionArgs.WIND.value: return [process_wind]
    elif condition_arg in ConditionArgs.ALL.value: return [process_temperature, process_humidity, process_wind]

def create_argument_parser(parser: argparse.ArgumentParser) -> None:
    parser = argparse.ArgumentParser(description="Get the current weather information for a city")

    parser.add_argument(
        "city", help="Name of the city to get the weather information for"
    )
    parser.add_argument(
        "-c",
        "--conditions",
        dest="conditions",
        metavar="CONDITION",
        nargs="+",
        default=DEFAULT_CONDITION_ARGS,
        choices=[c for c_enum in ConditionArgs for c in c_enum.value],
        help=f"Weather conditions to display. Choose between {', '.join([' or '.join(c.value) for c in ConditionArgs])}.",
    )

    parser.add_argument(
        "--api-key",
        help="API key for the OpenWeatherMap API",
    )

    return parser

def check_api_key(args) -> None:
    if not args.api_key:
        print("Please provide an API key with the --api-key option.")

def collect_processing_funcs(args) -> list[WeatherProcessingFn]:
    collected = []
    for user_defined_condition_arg in args.conditions:
        fns = map_condition_arg_to_weather_processing_funcs(user_defined_condition_arg)
        collected.extend(fns)

    return list(set(collected))

def main() -> None:
    parser = create_argument_parser()
    args = parser.parse_args()

    check_api_key(args)
    processing_funcs = collect_processing_funcs(args)

    if processing_funcs:
        # Fetch the data from the OpenMapWeather API
        weather_forecast = get_complete_forecast(
            http_get_fn=http_get, api_key=args.api_key, city=args.city
        )

        for processing_func in processing_funcs:
            processing_func(weather_forecast)

    else:
        # This will never happen because temperature is set as the default condition.
        print(
            f"Please specify at least one weather condition to display with the --conditions option."
        )


if __name__ == "__main__":
    main()
