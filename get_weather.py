import requests
import datetime as dt

from Types.InvalidUsage import InvalidUsage
from Types.WeatherTypes import ForecastWeatherDTO, CurrentWeatherDTO


def get_weather(url, is_current=False):
    response = requests.get(url)
    response_data = response.json()

    if is_current:
        weather = CurrentWeatherDTO(response_data["current"], response_data["location"])
    else:
        requested_location = response_data["location"]
        forecast_day = response_data["forecast"]["forecastday"][-1]
        pressure = forecast_day["hour"][0]["pressure_mb"]
        weather = ForecastWeatherDTO(requested_location, forecast_day["day"], pressure)

    if response.status_code == requests.codes.ok:
        return weather.get_dict()

    raise InvalidUsage(response.text, status_code=response.status_code)


def get_future_weather(rsa_key: str, location=None, date=None):
    url_base_url = "http://api.weatherapi.com"
    url_api = "future.json"
    url_api_version = "v1"

    url = f"{url_base_url}/{url_api_version}/{url_api}?key={rsa_key}&q={location}&dt={date}"
    return get_weather(url)


def get_nearest_weather(rsa_key: str, location=None, days=None):
    url_base_url = "http://api.weatherapi.com"
    url_api = "forecast.json"
    url_api_version = "v1"

    url = f"{url_base_url}/{url_api_version}/{url_api}?key={rsa_key}&q={location}&days={days}&aqi=no&alerts=no"
    return get_weather(url)


def get_current_weather(rsa_key: str, location=None):
    url_base_url = "http://api.weatherapi.com"
    url_api = "current.json"
    url_api_version = "v1"

    url = f"{url_base_url}/{url_api_version}/{url_api}?key={rsa_key}&q={location}&aqi=no"
    return get_weather(url, is_current=True)


def resolve_weather(rsa_key: str, location=None, date=None):
    diff = dt.datetime.strptime(date, "%Y-%m-%d") - dt.datetime.now() + dt.timedelta(days=1)

    if diff.days > 14:
        return get_future_weather(rsa_key, location=location, date=date)
    if diff.days > 0:
        return get_nearest_weather(rsa_key, location, diff.days)
    if diff.days == 0:
        return get_current_weather(rsa_key, location=location)
    return "Weather history is not implemented"
