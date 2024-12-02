import os

from flask import Flask, render_template, request
from geopy.geocoders import Nominatim

from additional import check_bad_weather
from weather_api import AccuWeatherAPI
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def result():
    start = request.form["start"]
    end = request.form["end"]

    try:
        # Определяем координаты городов через Nominatim
        geolocator = Nominatim(user_agent="red-project-2")
        start_location = geolocator.geocode(start)
        end_location = geolocator.geocode(end)

        # Проверяем, получили ли корректный ответ
        if (not start_location) or (not end_location):
            return render_template("index.html",
                                   error="Проверьте правильность написания городов")

        # Создание экземпляра класса AccuWeatherAPI с указанием личного (почти) API ключа
        weather_api = AccuWeatherAPI(API_KEY)

        # Получение ключей городов из AccuWeather API
        start_key = weather_api.get_location_key(start_location.latitude, start_location.longitude)
        end_key = weather_api.get_location_key(end_location.latitude, end_location.longitude)

        # Получение данных о погоде из AccuWeather API
        start_weather = weather_api.get_weather(start_key)
        end_weather = weather_api.get_weather(end_key)

        # Прогоняем прогнозы погоды через модель для вынесения вердикта о благоприятности погоды
        start_conditions = check_bad_weather(start_weather)
        end_conditions = check_bad_weather(end_weather)

        # Возвращаем пользователю html ответ
        return render_template("result.html", start=start, end=end,
                               start_weather=start_weather, end_weather=end_weather,
                               start_conditions=start_conditions, end_conditions=end_conditions)
    except Exception as e:
        print(f"Ошибка: {e}")

        # Пользователь остаётся на той же странцие и видит ошибку с советом
        return render_template("index.html",
                               error="Ошибка при получении данных о погоде. "
                                     "Повторите запрос немного позднее")


if __name__ == "__main__":
    app.run(debug=True,
            port=5000)
