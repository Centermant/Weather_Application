import random
import requests
import matplotlib.pyplot as plt
from datetime import datetime



class WeatherAPI:
    """
    Класс для работы с API погоды.
    """
    def __init__(self, api_key):
        self.api_key = api_key

    def search_cities(self, query):
        """
        Ищет города по запросу через API.
        """
        url = f'http://api.weatherapi.com/v1/search.json?key={self.api_key}&q={query}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            cities = []
            for item in data:
                country = item.get('country', '')
                region = item.get('region', '')
                name = item.get('name', '')
                city_info = f"{country} {region} {name}".strip()
                cities.append(city_info)
            return cities
        else:
            return []

    def get_weather_forecast(self, city):
        """
        Получает прогноз погоды для выбранного города.
        """
        request_line = (
            f"http://api.weatherapi.com/v1/forecast.json?"
            f"key={self.api_key}&"
            f"q={city}&"
            f"days=7&"
            f"aqi=no&"
            f"alerts=no&"
            f"lang=ru"
        )
        response = requests.get(request_line).json()
        return response

    def build_graphs(self, forecast_days):
        """
        Строит графики температуры и влажности на основе прогноза.
        """
        dates = [datetime.fromtimestamp(day['date_epoch']).strftime('%Y-%m-%d') for day in forecast_days]
        temperatures = [day['day']['avgtemp_c'] for day in forecast_days]
        humidity = [day['day']['avghumidity'] for day in forecast_days]

        # График температуры
        plt.figure(figsize=(10, 4))
        plt.plot(dates, temperatures, label='Средняя температура (°C)', marker='o', color='blue')
        plt.title('Прогноз средней температуры на неделю', fontsize=14)
        plt.xlabel('Дата', fontsize=12)
        plt.ylabel('Температура (°C)', fontsize=12)
        plt.xticks(rotation=45, fontsize=10)
        plt.legend(fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig('temperature_forecast.png', dpi=300, bbox_inches='tight')
        plt.close()

        # График влажности
        plt.figure(figsize=(10, 4))
        plt.plot(dates, humidity, label='Средняя влажность (%)', marker='s', color='orange')
        plt.title('Прогноз средней влажности на неделю', fontsize=14)
        plt.xlabel('Дата', fontsize=12)
        plt.ylabel('Влажность (%)', fontsize=12)
        plt.xticks(rotation=45, fontsize=10)
        plt.legend(fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig('humidity_forecast.png', dpi=300, bbox_inches='tight')
        plt.close()

    def extract_weather_data(self, forecast_days):
        """
        Извлекает данные о погоде из ответа API.
        """
        matrix_data = {
            "avgtemp_c": [],
            "condition_text": [],
            "condition_icon": [],
            "precipitation": [],
            "humidity": [],
            "air_quality_aqi": []
        }

        for day in forecast_days:
            matrix_data["avgtemp_c"].append(day['day']['avgtemp_c'])
            matrix_data["condition_text"].append(day['day']['condition']['text'])
            icon_url = f"https://cdn.weatherapi.com/weather/64x64/day/{day['day']['condition']['icon'].split('/')[-1]}"
            matrix_data["condition_icon"].append(icon_url)
            precipitation = "Да" if day['day']['daily_will_it_rain'] == 1 or day['day']['daily_will_it_snow'] == 1 else "Нет"
            matrix_data["precipitation"].append(precipitation)
            matrix_data["humidity"].append(day['day']['avghumidity'])
            air_quality_aqi = day.get('day', {}).get('air_quality', {}).get('pm2_5', 'N/A')
            matrix_data["air_quality_aqi"].append(air_quality_aqi)

        return matrix_data