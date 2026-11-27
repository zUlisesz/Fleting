"""Recetario Personal: UI declarativa con Flet 1.0 (componentes, hooks y ``page.render``).

    python3 main.py        # desde la carpeta recetario, o: flet run
"""

import flet as ft

from services import create_service
from ui.app import App


def main(page: ft.Page) -> None:
    page.title = "Recetario Personal"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.TEAL)
    page.bgcolor = ft.Colors.GREY_50
    page.window.min_width = 850
    page.window.min_height = 650
    page.render(App, create_service())


if __name__ == "__main__":
    ft.run(main)
