# Получение данных по API с сайта https://openweathermap.org/

import requests
from bs4 import BeautifulSoup

def get_weather_data(your_lat, your_lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={your_lat}&lon={your_lon}&appid=6ea87baba2926c3b67f03c31f0788731&units=metric&lang=ru"
    response = requests.get(url)
    response.raise_for_status()  # Проверка на ошибки HTTP
    return response.json()


def json_to_html(data):
    soup = BeautifulSoup("<html><body></body></html>", "html.parser")
    body = soup.find("body")

    # Добавление заголовка
    h1 = soup.new_tag("h1")
    h1.string = f"Погода в {data.get('name')}:"
    body.append(h1)

    # Добавление отдельных элементов данных
    for key, value in data.items():
        if key in ['coord', 'weather', 'base', 'main', 'visibility', 'wind', 'clouds', 'dt', 'sys', 'timezone', 'id']:
            p = soup.new_tag("p")
            p.string = f"{key.replace('_', ' ').title()}: {value}"
            body.append(p)

    # Возвращаем красиво отформатированный HTML
    return soup.prettify()


if __name__ == "__main__":
    your_lat = input("Введите широту интересующей точки (по умолчанию 56.844959): ") or "56.844959"
    your_lon = input("Введите долготу интересующей точки (по умолчанию 60.591204): ") or "60.591204"
    weather_data = get_weather_data(your_lat, your_lon)
    html_output = json_to_html(weather_data)
    print('Результат записан в файл sixth_task_result.html')

    with open(r"C:\Users\Данила\PycharmProjects\DE_practice1\lab1\result\sixth_task_result.html", "w", encoding="utf-8") as file:
        file.write(html_output)