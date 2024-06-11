from enum import Enum
import pandas as pd

class Sensor(Enum):
    ALL = "All"
    TEMPERATURE = "Temperature"
    HUMIDITY = "Humidity"
    CO2 = "CO2"

def read_data(name: str) -> pd.DataFrame:
    return pd.read_csv(name)

def read_sensor_input_from_user() -> Sensor:
    sensor_values = [s.value for s in Sensor]
    option = input(f"Choose between {', '.join(sensor_values)}:")
    try:
        return Sensor(option)
    except ValueError:
        raise ValueError(f'Option not valid, should be {', '.join(sensor_values)} but {option} given!')

def filter_data(data: pd.DataFrame, sensor_option: Sensor) -> pd.DataFrame:
    if sensor_option != Sensor.ALL:
        return data.loc[data["Sensor"] == sensor_option.value]
    else:
        return data

SENSOR_TO_PROCESSING_FUNCTION = {
    Sensor.TEMPERATURE: lambda x: x + 273.15,
    Sensor.HUMIDITY: lambda x: x / 100,
    Sensor.CO2: lambda x: x + 23,
}

def process_row(row: pd.Series) -> pd.Series:
    s = Sensor(row["Sensor"])
    fn = SENSOR_TO_PROCESSING_FUNCTION[s]
    row["Value"] = fn(row["Value"])
    return row

def process_data(data: pd.DataFrame) -> pd.DataFrame:
    return data.apply(process_row, axis=1)

def main() -> None:
    option = read_sensor_input_from_user()

    data = read_data("sensor_data.csv")
    data = filter_data(data, option)

    processed_data_single = process_data(data)

    print(processed_data_single)

if __name__ == "__main__":
    main()
