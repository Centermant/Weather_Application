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

# Переменные для погоды
TEMPERATURE = "-5 °C"  # Текущая температура
AIR_HUMIDITY = "82%"  # Влажность воздуха
WEATHER_ACTIVITY = "Пасмурно, небольшой снег"  # Описание погодных условий
UF_INDEX = "1 (Низкий)"  # Ультрафиолетовый индекс
AIR_QUALITY = "Умеренный"  # Качество воздуха
JOKES = [  # Список шуток для отображения
    "Почему снег такой белый? Потому что он вымыт Tide!",
    "Как называется любимый вид спорта снеговика? Боулинг!",
    "Зима — это когда все белые.",
    "Что говорит снежинка своей маме? Я падаю духом!",
    "Зачем снеговик пошел на дискотеку? Чтобы оттянуться!",
    "Почему пингвины не летают? Потому что есть авиакомпании!"
]

CITY_LIST = ["Москва", "Краснодар", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Сочи", "Казань", "Ростов-на-Дону"]

# Для картинки
IMAGE_URL = "https://cdn1.ozone.ru/s3/multimedia-m/6232237966.jpg"  # Ссылка на изображение


class WeatherApp:
    """
    Основной класс приложения "Погода".

    Управляет навигацией между формами выбора города и отображения погоды,
    а также предоставляет общий доступ к данным и функциям.
    """

    def __init__(self, page: ft.Page):
        """
        Инициализирует приложение "Погода".

        Args:
            page: Объект страницы Flet.
        """
        self.page = page
        self.selected_city = None
        self.weather_view = None

    def did_mount(self):
        """Вызывается при монтировании приложения. Устанавливает начальный маршрут."""
        self.page.go("/city_select")

    def route_change(self, route):
        """
        Обрабатывает изменение маршрута в приложении.

        Args:
            route: Новый маршрут.
        """
        self.page.views.clear()
        if self.page.route == "/city_select":
            self.page.views.append(CitySelectForm(self).build_view())
        elif self.page.route == "/weather":
            if self.weather_view is None:
                self.weather_view = WeatherView(self)
            self.page.views.append(self.weather_view.build_view())
        self.page.update()

    def go_weather_view(self):
        """Переходит к представлению погоды."""
        self.page.go("/weather")

    def build(self):
        """Создает основной элемент управления для приложения."""
        self.page.on_route_change = self.route_change
        return ft.Text("Главный виджет приложения")


class CitySelectForm:
    """
    Форма выбора города.

    Позволяет пользователю ввести название города и выбрать его из списка предложений.
    """

    def __init__(self, app: WeatherApp):
        """
        Инициализирует форму выбора города.

        Args:
            app: Объект приложения "Погода".
        """
        self.app = app
        self.city_input = ft.TextField(
            label="Введите свой город",
            label_style=ft.TextStyle(color=TEXT_COLOR, font_family=FONT_FAMILY),
            color=TEXT_COLOR,
            bgcolor=CITY_INPUT_BG_COLOR,
            border_color=TEXT_COLOR,
            width=ELEMENT_WIDTH,
            on_change=self.update_suggestions
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
                color={"": BUTTON_TEXT_COLOR},
                bgcolor={"": BUTTON_COLOR},
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                text_style=ft.TextStyle(font_family=FONT_FAMILY, size=16),
            ),
        )
        self.city_list = CITY_LIST

    def update_suggestions(self, e):
        """Обновляет список предложений городов на основе введенного текста."""
        search_term = self.city_input.value.lower()

        if not search_term:
            self.suggestion_list.visible = False
            self.app.page.update()
            return

        suggestions = [
            ft.TextButton(
                text=city,
                width=ELEMENT_WIDTH,
                on_click=lambda e, city=city: self.select_suggestion(city),
            )
            for city in self.city_list
            if search_term in city.lower()
        ]

        list_view = self.suggestion_list.content
        list_view.controls = suggestions

        self.suggestion_list.visible = len(suggestions) > 0
        self.app.page.update()

    def select_suggestion(self, city):
        """Выбирает город из списка предложений."""
        self.city_input.value = city
        self.suggestion_list.visible = False
        self.app.page.update()

    def confirm_city_selection(self, e):
        """Подтверждает выбор города и переходит к окну погоды."""
        self.app.selected_city = self.city_input.value
        print(f"Выбран город: {self.app.selected_city}")
        self.app.go_weather_view()

    def build_view(self):
        """Создает представление формы выбора города."""
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
    """
    Представление погоды.

    Отображает информацию о погоде для выбранного города, включая температуру, влажность,
    состояние погоды, УФ-индекс и качество воздуха.
    """

    def __init__(self, app: WeatherApp):
        """
        Инициализирует представление погоды.

        Args:
            app: Объект приложения "Погода".
        """
        self.app = app
        self.random_joke = random.choice(JOKES)
        self.all_columns = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье",
                            "Дополнительный", "Еще один"]
        self.all_data = [
            ["Солнечно"] * len(self.all_columns),
            ["25°C"] * len(self.all_columns),
            ["Ветер"] * len(self.all_columns),
            ["Облачно"] * len(self.all_columns),
            ["Дождь"] * len(self.all_columns),
        ]
        self.cols_per_page = 5
        self.current_offset = 0

    def create_row(self, row_data):
        """Создает строку таблицы."""
        return ft.Row(
            [ft.Text(cell, width=100) for cell in row_data],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def get_current_columns(self):
        """Возвращает список отображаемых столбцов."""
        return self.all_columns[self.current_offset:self.current_offset + self.cols_per_page]

    def get_current_rows(self):
        """Возвращает список отображаемых строк."""
        current_cols = self.get_current_columns()
        rows = []
        for row_data in self.all_data:
            current_row = row_data[self.current_offset:self.current_offset + self.cols_per_page]
            rows.append(self.create_row(current_row))
        return rows

    def update_table(self):
        """Обновляет таблицу с текущими данными."""
        self.header = ft.Row(
            [ft.Text(col, weight=ft.FontWeight.BOLD, width=100) for col in self.get_current_columns()],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.table_content.controls = [self.header] + self.get_current_rows()
        self.app.page.update()

    def scroll_left(self, e):
        """Сдвигает таблицу влево."""
        self.current_offset = max(0, self.current_offset - 1)
        self.update_table()

    def scroll_right(self, e):
        """Сдвигает таблицу вправо."""
        self.current_offset = min(len(self.all_columns) - self.cols_per_page, self.current_offset + 1)
        self.update_table()

    def build_view(self):
        """Создает представление окна погоды."""
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
            expand=True,
            bgcolor=INFO_BOX_BG_COLOR,
            border_radius=10,
            padding=10,
            alignment=ft.alignment.center
        )

        self.header = ft.Row(
            [ft.Text(col, weight=ft.FontWeight.BOLD, width=100) for col in self.get_current_columns()],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.table_content = ft.Column(controls=[self.header] + self.get_current_rows())

        self.button_row = ft.Row(
            [
                ft.IconButton(ft.icons.KEYBOARD_ARROW_LEFT, on_click=self.scroll_left),
                ft.IconButton(ft.icons.KEYBOARD_ARROW_RIGHT, on_click=self.scroll_right),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        panel2 = ft.Container(
            content=ft.Column(
                [
                    self.button_row,
                    self.table_content,
                    ft.Container(height=1, expand=True),
                ],
                height=300
            ),
            expand=True,
            bgcolor=INFO_BOX_BG_COLOR,
            border_radius=10,
            padding=10,
        )

        panel3 = ft.Container(
            content=ft.Image(src=IMAGE_URL, fit=ft.ImageFit.CONTAIN),
            expand=True,
            bgcolor=INFO_BOX_BG_COLOR,
            border_radius=10,
            padding=10
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
            expand=True,
            bgcolor=INFO_BOX_BG_COLOR,
            border_radius=10,
            padding=10,

        )

        panel5 = ft.Container(
            content=ft.Text(self.random_joke, color=TEXT_COLOR, text_align=ft.TextAlign.CENTER),
            expand=True,
            bgcolor=INFO_BOX_BG_COLOR,
            border_radius=10,
            padding=10,
            alignment=ft.alignment.center
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
    """Главная функция приложения."""
    page.title = "Погода"
    page.bgcolor = BACKGROUND_COLOR
    page.theme = ft.Theme(font_family=FONT_FAMILY)
    page.window_resizable = True
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