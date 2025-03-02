import flet as ft
import random

# Стилизация
BACKGROUND_COLOR = "#E8F5E9"  # Светло-зеленый фон
TEXT_COLOR = "#212121"  # Темно-серый цвет текста
FONT_FAMILY = "Roboto"  # Шрифт
BUTTON_COLOR = "#4CAF50"  # Зеленый цвет кнопки
BUTTON_TEXT_COLOR = "#FFFFFF"  # Белый цвет текста кнопки
CITY_INPUT_BG_COLOR = "#FFFFFF"  # Белый фон поля ввода города
CITY_SUGGESTION_BG_COLOR = "#EEEEEE"  # Светло-серый фон для подсказки
INFO_BOX_BG_COLOR = "#FFFFFF"  # Белый фон для инф. блоков
INFO_BOX_TEXT_COLOR = TEXT_COLOR
ELEMENT_WIDTH = 300  # Ширина основных элементов (поле ввода, подсказка, кнопка)
FORM_PADDING = 20  # Отступ от нижнего края для кнопки
PANEL_HEIGHT = 100  # Высота каждой панели
SMALL_PANEL_HEIGHT = 50  # Высота маленьких панелей
WEATHER_VIEW_WIDTH = 400  # Ширина окна второй формы

# Переменные для погоды, данные из апишечки сюды
TEMPERATURE = "-5 °C"
AIR_HUMIDITY = "82%"
WEATHER_ACTIVITY = "Пасмурно, небольшой снег"
UF_INDEX = "1 (Низкий)"
AIR_QUALITY = "Умеренный"
JOKES = [
    "Что такое бутерброд",
    "Пара в маке?",
    "Зима — это когда все белые."
]

CITY_LIST = ["Москва", "Краснодар", "Санкт-Петербург", "Новосибирск", "Екатеринбург"]


class WeatherApp:
    """Класс, управляющий приложением погоды."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.selected_city = None

    def did_mount(self):
        """Устанавливает начальную страницу."""
        self.page.go("/city_select")

    def route_change(self, route):
        """Определяет вид для отображения в зависимости от маршрута."""
        self.page.views.clear()
        if self.page.route == "/city_select":
            self.page.views.append(CitySelectForm(self).build_view())
        elif self.page.route == "/weather":
            self.page.views.append(WeatherView(self).build_view())
        self.page.update()

    def go_weather_view(self):
        """Переходит на страницу погоды."""
        self.page.go("/weather")

    def build(self):
        self.page.on_route_change = self.route_change
        return ft.Text("Главный виджет приложения")


class CitySelectForm:
    """Класс, представляющий форму выбора города."""

    def __init__(self, app: WeatherApp):
        self.app = app
        self.city_input = ft.TextField(
            label="Введите или выберите свой город",
            label_style=ft.TextStyle(color=TEXT_COLOR, font_family=FONT_FAMILY),
            color=TEXT_COLOR,
            bgcolor=CITY_INPUT_BG_COLOR,
            border_color=TEXT_COLOR,
            width=ELEMENT_WIDTH,
        )
        self.suggestion_text = ft.Text("", color=TEXT_COLOR)
        self.suggestion_container = ft.Container(
            content=self.suggestion_text,
            bgcolor=CITY_SUGGESTION_BG_COLOR,
            width=ELEMENT_WIDTH,
            padding=10,
            visible=False,
            alignment=ft.alignment.center,
        )
        self.confirm_button = ft.ElevatedButton(
            text="Подтвердить выбор",
            on_click=self.confirm_city_selection,
            style=ft.ButtonStyle(
                color={"": BUTTON_TEXT_COLOR},
                bgcolor={"": BUTTON_COLOR},
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                text_style=ft.TextStyle(font_family=FONT_FAMILY, size=16),
            ),
        )
        self.city_list = CITY_LIST

    def update_suggestions(self, e):
        """Обновляет список предложений городов."""
        best_match = None
        if self.city_input.value:
            for city in self.city_list:
                if self.city_input.value.lower() in city.lower():
                    best_match = city
                    break

        if best_match:
            self.suggestion_text.value = best_match
            self.suggestion_container.visible = True
        else:
            self.suggestion_text.value = ""
            self.suggestion_container.visible = False

        self.app.page.update()

    def city_selected(self, e):
        """Обрабатывает выбор города из списка."""
        self.city_input.value = self.suggestion_text.value
        self.suggestion_container.visible = False
        self.app.page.update()

    def confirm_city_selection(self, e):
        """Подтверждает выбор города и переходит к окну погоды."""
        self.app.selected_city = self.city_input.value
        print(f"Выбран город: {self.app.selected_city}")
        self.app.go_weather_view()

    def build_view(self):
        self.city_input.on_change = self.update_suggestions
        self.suggestion_container.on_click = self.city_selected
        main_column = ft.Column(
            [
                ft.Container(expand=True),  # Spacer
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
                self.suggestion_container,
                ft.Container(expand=True),  # Spacer
                self.confirm_button,
                ft.Container(height=FORM_PADDING),  # Отступ снизу для кнопки
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
        return ft.View(
            route="/city_select",
            controls=[main_column],
        )


class WeatherView:
    """Класс, представляющий окно с отображением погоды."""

    def __init__(self, app: WeatherApp):
        self.app = app
        self.random_joke = random.choice(JOKES)

    def build_view(self):
        city_text = ft.Text(f"Погода в городе: {self.app.selected_city or 'Не выбран'}",
                                 color=TEXT_COLOR, font_family=FONT_FAMILY, size=20, weight=ft.FontWeight.BOLD)

        panel1 = ft.Container(
            content=ft.Column(
                [
                    ft.Text(TEMPERATURE, color=TEXT_COLOR, weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER),
                    ft.Row(
                        [
                            ft.Text(AIR_HUMIDITY, color=TEXT_COLOR, width=150, text_align=ft.TextAlign.LEFT),
                            ft.Text(WEATHER_ACTIVITY, color=TEXT_COLOR, width=150, text_align=ft.TextAlign.RIGHT),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=2
            ),
            width=WEATHER_VIEW_WIDTH,
            expand=True,
            bgcolor=INFO_BOX_BG_COLOR,
            border_radius=10,
            padding=10,
            alignment=ft.alignment.center
        )

        panel2 = ft.Container(
            width=WEATHER_VIEW_WIDTH,
            expand=True,
            bgcolor=INFO_BOX_BG_COLOR,
            border_radius=10,
        )

        panel3 = ft.Container(
            width=WEATHER_VIEW_WIDTH,
            expand=True,
            bgcolor=INFO_BOX_BG_COLOR,
            border_radius=10,
        )

        panel4 = ft.Container(
            content=ft.Column(
                [
                    ft.Text(f"UF индекс: {UF_INDEX}", color=TEXT_COLOR, text_align=ft.TextAlign.CENTER),
                    ft.Text(f"Качество воздуха: {AIR_QUALITY}", color=TEXT_COLOR, text_align=ft.TextAlign.CENTER),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=ELEMENT_WIDTH / 2,
            expand=True,
            bgcolor=INFO_BOX_BG_COLOR,
            border_radius=10,
            padding=10,

        )

        panel5 = ft.Container(
            content=ft.Text(self.random_joke, color=TEXT_COLOR, text_align=ft.TextAlign.CENTER),
            width=ELEMENT_WIDTH / 2,
            expand=True,
            bgcolor=INFO_BOX_BG_COLOR,
            border_radius=10,
            padding=10,
            alignment=ft.alignment.center,
        )

        back_button = ft.ElevatedButton(
            text="Выбрать другой город",
            on_click=lambda _: self.app.page.go("/city_select"),
            style=ft.ButtonStyle(
                color={"": BUTTON_TEXT_COLOR},
                bgcolor={"": BUTTON_COLOR},
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                text_style=ft.TextStyle(font_family=FONT_FAMILY, size=16),
            ),
        )

        main_column = ft.Column(
            [
                city_text,
                panel1,
                panel2,
                panel3,
                ft.Row([panel4, panel5], alignment=ft.MainAxisAlignment.CENTER, expand=True),
                back_button,
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
    page.window_width = 400
    page.window_height = 600
    page.window_resizable = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def route_change(route):
        app.route_change(route)

    page.on_route_change = route_change
    app = WeatherApp(page)
    app.did_mount()
    page.add(app.build())

if __name__ == "__main__":
    ft.app(target=main)