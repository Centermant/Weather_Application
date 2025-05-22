import requests
import pygal
import cairosvg
from datetime import datetime
from pygal.style import Style



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

        # Общий стиль графиков
        custom_style = Style(
            font_family='Roboto',
            title_font_size=14,
            label_font_size=12,
            major_label_font_size=10,
            colors=('#2196F3', '#FF9800')  # Синий и оранжевый
        )

        # График температуры
        chart_temp = pygal.Line(
            style=custom_style,
            x_label_rotation=45,
            show_legend=False,
            width=800,
            height=300,
            margin=20,
            explicit_size=True
        )
        chart_temp.title = 'Прогноз температуры (°C)'
        chart_temp.x_labels = dates
        chart_temp.add('', temperatures)
        chart_temp.render_to_file('temperature_forecast.svg')
        cairosvg.svg2png(url='temperature_forecast.svg', write_to='temperature_forecast.png')

        # График влажности
        chart_hum = pygal.Line(
            style=custom_style,
            x_label_rotation=45,
            show_legend=False,
            width=800,
            height=300,
            margin=20,
            explicit_size=True
        )
        chart_hum.title = 'Прогноз влажности (%)'
        chart_hum.x_labels = dates
        chart_hum.add('', humidity)
        chart_hum.render_to_file('humidity_forecast.svg')
        cairosvg.svg2png(url='humidity_forecast.svg', write_to='humidity_forecast.png')


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