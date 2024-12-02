import requests

BASE_URL = "https://dataservice.accuweather.com"


class AccuWeatherAPI:
    """
    Класс для взаимодействия с AccuWeather API
    """

    def __init__(self,
                 api_key: str):
        self.api_key = api_key

    def get_location_key(self,
                         latitude: float,
                         longitude: float) -> str:
        """
        Получение внутреннего кода локации в AccuWeather
        """
        url = f"{BASE_URL}/locations/v1/cities/geoposition/search"

        params = {
            "apikey": self.api_key,
            "q": f"{latitude},{longitude}",
            "language": "ru"
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        return data["Key"]

    def get_weather(self,
                    location_key: str) -> dict:
        """
        Получение прогноза погоды в текущем городе
        """
        url = f"{BASE_URL}/forecasts/v1/hourly/1hour/{location_key}"

        params = {
            "apikey": self.api_key,
            "language": "ru",
            "metric": True,
            "details": True
        }

        response = requests.get(url,
                                params=params)
        response.raise_for_status()

        data = response.json()[0]

        weather_data = {
            "temperature": data["Temperature"]["Value"],
            "wind_speed": data["Wind"]["Speed"]["Value"],
            "precipitation_probability": data["PrecipitationProbability"]
        }

        return weather_data
