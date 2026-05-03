import os
import requests
from dotenv import load_dotenv
from pprint import pprint
from datetime import datetime

# Словарь перевода значений направления ветра
DIRECTION_TRANSFORM = {
    'n': 'северное',
    'nne': 'северо - северо - восточное',
    'ne': 'северо - восточное',
    'ene': 'восточно - северо - восточное',
    'e': 'восточное',
    'ese': 'восточно - юго - восточное',
    'se': 'юго - восточное',
    'sse': 'юго - юго - восточное',
    's': 'южное',
    'ssw': 'юго - юго - западное',
    'sw': 'юго - западное',
    'wsw': 'западно - юго - западное',
    'w': 'западное',
    'wnw': 'западно - северо - западное',
    'nw': 'северо - западное',
    'nnw': 'северо - северо - западное',
    'c': 'штиль',
}


def current_weather(lat:float, lon:float) -> dict:
    """
    Функция работает с сервисом погоды www.weatherapi.com.
    Входные данные - координаты на карте: lat - широта, lon - долгота (числа с плавающей точкой).
    Функция выполняет запрос к сервису погоды на основании входных данных с использованием ключа (токена).
    Функция осуществляет следующие преобразования: атмосферное давление (миллибары -> мм.рт.ст), скорость ветра (км/ч -> м/с).
    Выходные данные - словарь.
    """
    # token = ''  # Вставить ваш токен из api.weatherapi.com
    load_dotenv() # Считать ключ из файла .env в память
    token = os.getenv("WEATHER_API_KEY") # Передать значение ключа переменной token
    url = f"https://api.weatherapi.com/v1/current.json?key={token}&q={lat},{lon}"
    response = requests.get(url)
    data = response.json() #

    # "Свежесть" прогноза
    local_time = data['location']['localtime_epoch']
    updated_time = data['current']['last_updated_epoch']
    l_time = datetime.fromtimestamp(local_time).strftime("%d.%m %H:%M")
    u_time = datetime.fromtimestamp(updated_time).strftime("%d.%m %H:%M")
    print(f"Местное время: {l_time}\nВремя последнего обновления: {u_time}")

    # Данная реализация приведена для api.weatherapi.com
    result = {
        'city': data['location']['name'],  # Город
        'time': data['current']['last_updated'],  # Время обновления данных
        'temp': data['current']['temp_c'],  # TODO Реализовать вычисление температуры из данных полученных от API
        'feels_like_temp': data['current']['feelslike_c'],  # TODO Реализовать вычисление ощущаемой температуры из данных полученных от API
        'pressure': round((float(data['current']['pressure_mb']) * 0.75), 1),  # TODO Реализовать вычисление давления из данных полученных от API
        'humidity': data['current']['humidity'],  # TODO Реализовать вычисление влажности из данных полученных от API
        'wind_speed': round((float(data['current']['wind_kph']) / 3.6), 1),  # TODO Реализовать вычисление скорости ветра из данных полученных от API
        'wind_gust': round((float(data['current']['gust_kph']) / 3.6), 1),  # TODO Реализовать вычисление скорости порывов ветка из данных полученных от API
        'wind_dir': DIRECTION_TRANSFORM.get(data['current']['wind_dir'].lower()),  # Направление ветра
    }
    return result


if __name__ == "__main__":
    #pprint(current_weather(59.93, 30.31))  # Проверка работы для координат Санкт-Петербурга
    pprint(current_weather(45.62, 63.31)) # Координаты Байконура
