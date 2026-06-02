import os
import requests
from dotenv import load_dotenv
from pprint import pprint  # Чтобы сложный словарь вывести читаемо для человека

load_dotenv() # Считать ключ из файла .env в память
token = os.getenv("WEATHER_API_KEY") # Передать значение ключа переменной token
# Координаты города Великий Новгород:
lat = "58.52"  # широта в градусах
lon = "31.27"  # долгота в градусах

url = f"https://api.weatherapi.com/v1/current.json?key={token}&q={lat},{lon}"
response = requests.get(url)  # отправление GET запроса и получение ответа от сервера
pprint(response.json())  # получение JSON из ответа