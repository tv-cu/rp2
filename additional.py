def check_bad_weather(weather) -> str:
    """
    Функция с моделью для определения неблагоприятных погодных условий.
    """
    if weather["temperature"] > 35:
        return "В городе очень жарко"

    if weather["temperature"] < 0:
        return "В городе холодно"

    if weather["wind_speed"] > 50:
        return "Высокая скорость ветра"

    if weather["precipitation_probability"] > 70:
        return "Высокая вероятность осадков"

    return "Погодные условия благоприятные"
