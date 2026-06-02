import requests

url = 'http://127.0.0.1:8000/weather/'

try:
    response = requests.get(url)

    # Проверяем, что сервер ответил успешно (код 200)
    if response.status_code == 200:
        # Конвертируем JSON-строку в словарь Python
        weather_data = response.json()
        # Вывод на печать
        for key, value in weather_data.items():
            print(f"{key:<20}: {value}")

    else:
        print(f"Сервер вернул ошибку: {response.status_code}")

except requests.exceptions.ConnectionError:
    print("Ошибка подключения! Убедитесь, что сервер Django запущен.")
