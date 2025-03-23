import flet as ft
from frontend import BACKGROUND_COLOR, FONT_FAMILY, WeatherApp

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