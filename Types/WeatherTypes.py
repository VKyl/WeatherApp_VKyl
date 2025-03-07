from abc import ABC, abstractmethod


class ABWeatherDTO(ABC):
    def __init__(self, *args):
        self._result = self._parse_date(*args)

    def get_dict(self):
        return self._result

    @abstractmethod
    def _parse_date(self, *args):
        pass


class ForecastWeatherDTO(ABWeatherDTO):
    def __init__(self, requested_location, day_info, pressure):
        super().__init__(requested_location, day_info, pressure)

    def _parse_date(self, *args):
        return {
            "temp_c": args[1]["avgtemp_c"],
            "wind_kph": args[1]["maxwind_kph"],
            "pressure_mb": args[2],
            "humidity": args[1]["avghumidity"],
            "cast_location": f'{args[0]["name"]}, {args[0]["region"]}',
            "icon": args[1]["condition"]["icon"]
        }


class CurrentWeatherDTO(ABWeatherDTO):
    def __init__(self, current_info, location):
        super().__init__(current_info, location)

    def _parse_date(self, *args):
        return {
            "temp_c": args[0]["temp_c"],
            "wind_kph": args[0]["wind_kph"],
            "pressure_mb": args[0]["pressure_mb"],
            "humidity": args[0]["humidity"],
            "cast_location": f'{args[1]["name"]}, {args[1]["region"]}',
            "icon": args[0]["condition"]["icon"]
        }
