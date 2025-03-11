import random
import flet as ft
from backend import WeatherAPI

BACKGROUND_COLOR = "#E8F5E9"
TEXT_COLOR = "#212121"
FONT_FAMILY = "Roboto"
BUTTON_COLOR = "#4CAF50"
BUTTON_TEXT_COLOR = "#FFFFFF"
CITY_INPUT_BG_COLOR = "#FFFFFF"
CITY_SUGGESTION_BG_COLOR = "#EEEEEE"
INFO_BOX_BG_COLOR = "#99e9ea"
ELEMENT_WIDTH = 300
FORM_PADDING = 20
PANEL_HEIGHT = 100
SMALL_PANEL_HEIGHT = 50
IMAGE_URL = \
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-uJnjLhTwYJS5z6Km36wDZzoOunLyAzi-DQ&s"
STIHI = [
    "«ПАЗик»\nПо дороге поселковой,\nКолеся февральский снег,\nВ ПАЗике давно не новом\nНовый ехал человек.\n❮Отрывок❯\nАвтор - Иван Тананин",
    "«ПАЗик»\nПоле снегом, как сорочкой\nСлепит белым сквозь окно,\nВремя будто бы бессрочно,\nА как глянешь - нет его.\n❮Отрывок❯\nАвтор - Иван Тананин",
    "«ПАЗик»\nПечка тёплая в салоне,\nНе охота выходить.\nЗаревёт февраль на склоне,\nДо рассвета будет выть.\n❮Отрывок❯\nАвтор - Иван Тананин",
    "«ПАЗик»\nЯ приеду, выйду, спрыгну\nИ пойду себе домой.\nДома буду, дома был я.\nТам дом мой и здесь дом мой.\n❮Отрывок❯\nАвтор - Иван Тананин"
]


class WeatherApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.selected_city = None
        self.weather_view = None
        self.api = WeatherAPI(api_key="7ab029060bfd469aa0a90503250403")

    def did_mount(self):
        self.page.go("/city_select")

    def route_change(self, route):
        self.page.views.clear()
        if self.page.route == "/city_select":
            self.page.views.append(CitySelectForm(self).build_view())
        elif self.page.route == "/weather":
            if self.weather_view is None:
                self.weather_view = WeatherView(self)
            self.page.views.append(self.weather_view.build_view)
        self.page.update()

    def go_weather_view(self):
        self.page.go("/weather")

    def build(self):
        self.page.on_route_change = self.route_change
        self.did_mount()
        return ft.Container()


class CitySelectForm:
    def __init__(self, app: WeatherApp):
        self.app = app
        self.city_input = ft.TextField(
            label="Введите свой город",
            label_style=ft.TextStyle(color=TEXT_COLOR, font_family=FONT_FAMILY),
            color=TEXT_COLOR,
            bgcolor=CITY_INPUT_BG_COLOR,
            border_color=TEXT_COLOR,
            width=ELEMENT_WIDTH,
            on_change=self.update_suggestions,
            value=''
        )
        self.suggestion_list = ft.Container(
            content=ft.ListView(
                height=150,
                width=ELEMENT_WIDTH,
                controls=[],
                padding=5,
                spacing=2,
            ),
            bgcolor=INFO_BOX_BG_COLOR,
            border_radius=10,
            width=ELEMENT_WIDTH,
            visible=False
        )
        self.confirm_button = ft.ElevatedButton(
            text="Подтвердить выбор",
            on_click=self.confirm_city_selection,
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                text_style=ft.TextStyle(font_family=FONT_FAMILY, size=16),
            ),
        )

    def update_suggestions(self, e):
        search_term = self.city_input.value.lower()
        if not search_term:
            self.suggestion_list.visible = False
            self.app.page.update()
            return

        if len(search_term) < 3:
            suggestions = [
                ft.TextButton(
                    text=f"Введите ещё {3 - len(search_term)} символа",
                    width=ELEMENT_WIDTH,
                )
            ]
        else:
            cities = self.app.api.search_cities(search_term)
            suggestions = [
                ft.TextButton(
                    text=city,
                    width=ELEMENT_WIDTH,
                    on_click=lambda e, city=city: self.select_suggestion(city),
                )
                for city in cities
            ]

        list_view = self.suggestion_list.content
        list_view.controls = suggestions
        self.suggestion_list.visible = len(suggestions) > 0
        self.app.page.update()

    def select_suggestion(self, city):
        self.city_input.value = city
        self.suggestion_list.visible = False
        self.app.page.update()

    def confirm_city_selection(self, e):
        self.app.selected_city = self.city_input.value
        self.app.go_weather_view()

    def build_view(self):
        return ft.View(
            route="/city_select",
            controls=[
                ft.Column(
                    [
                        ft.Container(expand=True),
                        ft.Row(
                            [
                                ft.Text(
                                    "Выберите свой город",
                                    color=TEXT_COLOR,
                                    font_family=FONT_FAMILY,
                                    size=20,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        self.city_input,
                        self.suggestion_list,
                        ft.Container(expand=True),
                        self.confirm_button,
                        ft.Container(height=FORM_PADDING),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                )
            ],
        )


class WeatherView:
    def __init__(self, app: WeatherApp):
        self.app = app
        self.random_joke = random.choice(STIHI)
        self.all_columns = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

        forecast_data = self.app.api.get_weather_forecast(self.app.selected_city)
        forecast_days = forecast_data['forecast']['forecastday']
        self.app.api.build_graphs(forecast_days)
        self.all_data = self.app.api.extract_weather_data(forecast_days)

        self.TEMPERATURE = self.all_data['avgtemp_c'][0]
        self.WEATHER_ACTIVITY = self.all_data['condition_text'][0]
        self.WEATHER_ICON = self.all_data['condition_icon'][0]
        self.AIR_HUMIDITY = self.all_data['humidity'][0]
        self.AQI = self.all_data['air_quality_aqi'][0]

    def create_row(self, row_data):
        return ft.Row(
            [ft.Text(cell, width=100) for cell in row_data],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def get_current_rows(self):
        rows = []
        rows.append(self.create_row(self.all_data['avgtemp_c']))
        rows.append(self.create_row(self.all_data['condition_text']))
        rows.append(self.create_row([f"Осадки: {x}" for x in self.all_data['precipitation']]))
        return rows

    @property
    def build_view(self):
        back_button = ft.ElevatedButton(
            text="Выбрать другой город",
            on_click=lambda _: self.app.page.go("/city_select"),
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                text_style=ft.TextStyle(font_family=FONT_FAMILY, size=16),
            ),
        )

        city_text_container = ft.Container(
            content=ft.Text(
                f"Погода в городе: {self.app.selected_city or 'Не выбран'}",
                color=TEXT_COLOR,
                font_family=FONT_FAMILY,
                size=20,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                max_lines=2,
                overflow=ft.TextOverflow.VISIBLE,
            ),
            expand=True,
            alignment=ft.alignment.center,
        )

        panel1 = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        f"Среднесуточная температура\n{self.TEMPERATURE}",
                        color=TEXT_COLOR,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Row(
                        [
                            ft.Text(
                                f"Средняя влажность\n{self.AIR_HUMIDITY}%",
                                color=TEXT_COLOR,
                                width=150,
                                text_align=ft.TextAlign.LEFT,
                            ),
                            ft.Text(
                                self.WEATHER_ACTIVITY,
                                color=TEXT_COLOR,
                                width=150,
                                text_align=ft.TextAlign.RIGHT,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=2,
            ),
            expand=True,
            bgcolor=INFO_BOX_BG_COLOR,
            border_radius=10,
            padding=10,
            alignment=ft.alignment.center,
        )

        self.header = ft.Row(
            [ft.Text(col, weight=ft.FontWeight.BOLD, width=100) for col in self.all_columns],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.table_content = ft.Column(controls=[self.header] + self.get_current_rows())

        self.offset_x_table = 0

        def on_pan_update_table(e: ft.DragUpdateEvent):
            self.offset_x_table -= e.delta_x / 10
            self.offset_x_table = max(0, min(self.offset_x_table, self.max_offset))
            self.table_container.content.offset = ft.Offset(-self.offset_x_table / 100, 0)
            self.app.page.update()

        def on_pan_end_table(e: ft.DragEndEvent):
            pass

        self.table_container = ft.GestureDetector(
            content=ft.Container(
                content=self.table_content,
                offset=ft.Offset(0, 0),
            ),
            on_pan_update=on_pan_update_table,
            on_pan_end=on_pan_end_table,
            drag_interval=10,
        )

        panel2 = ft.Container(
            content=ft.Row(
                [self.table_container],
                alignment=ft.MainAxisAlignment.CENTER,
                height=300,
            ),
            expand=True,
            bgcolor=INFO_BOX_BG_COLOR,
            border_radius=10,
            padding=10,
        )

        self.offset_x_graphs = 0

        def on_pan_update_graphs(e: ft.DragUpdateEvent):
            self.offset_x_graphs -= e.delta_x / 10
            self.offset_x_graphs = max(0, min(self.offset_x_graphs, self.max_offset))
            self.graphs_container.content.offset = ft.Offset(-self.offset_x_graphs / 100, 0)
            self.app.page.update()

        def on_pan_end_graphs(e: ft.DragEndEvent):
            pass

        self.graphs_container = ft.GestureDetector(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Image(
                            src="temperature_forecast.png",
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        ft.Image(
                            src="humidity_forecast.png",
                            fit=ft.ImageFit.CONTAIN,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                offset=ft.Offset(0, 0),
            ),
            on_pan_update=on_pan_update_graphs,
            on_pan_end=on_pan_end_graphs,
            drag_interval=10,
        )

        panel3 = ft.Container(
            content=self.graphs_container,
            expand=True,
            bgcolor=INFO_BOX_BG_COLOR,
            border_radius=10,
            padding=10,
            alignment=ft.alignment.center,
        )

        panel4 = ft.Container(
            content=ft.Column(
                [
                    ft.Image(
                        src=IMAGE_URL,
                        expand=True,
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True,
            bgcolor=INFO_BOX_BG_COLOR,
            border_radius=10,
            padding=10,
            alignment=ft.alignment.center,
        )

        panel5 = ft.Container(
            content=ft.Text(
                self.random_joke,
                color=TEXT_COLOR,
                text_align=ft.TextAlign.CENTER,
            ),
            expand=True,
            bgcolor=INFO_BOX_BG_COLOR,
            border_radius=10,
            padding=10,
            alignment=ft.alignment.center,
        )

        def exit_program(e):
            self.app.page.window.close()

        graph_width = 300
        self.max_offset = graph_width * 2 + 10

        main_column = ft.Column(
            [
                ft.Row(
                    [back_button, city_text_container, ft.ElevatedButton(text="X", on_click=exit_program)],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                panel1,
                panel2,
                panel3,
                ft.Row([panel4, panel5], alignment=ft.MainAxisAlignment.CENTER, expand=True),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

        return ft.View(
            route="/weather",
            controls=[main_column],
        )


def main(page: ft.Page):
    page.title = "Погода"
    page.bgcolor = BACKGROUND_COLOR
    page.theme = ft.Theme(font_family=FONT_FAMILY)
    page.window_resizable = False
    page.window.full_screen = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def route_change(route):
        if app.weather_view:
            app.weather_view.update_table()
        app.route_change(route)

    page.on_route_change = route_change
    app = WeatherApp(page)
    app.did_mount()
    page.add(app.build())


if __name__ == "__main__":
    ft.app(target=main)