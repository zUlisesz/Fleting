"""Punto de entrada del catálogo de componentes.

Ejecutar con cualquiera de:

    flet run main.py             # desde esta carpeta
    python3 main.py              # desde esta carpeta
    python3 -m components.main   # desde la carpeta que contiene `components/`
"""

import sys
from pathlib import Path

import flet as ft

if not __package__:  # Ejecutado como script: hace importable `components`.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from components.app import App  # noqa: E402
from components.theme import COLORS  # noqa: E402


def main(page: ft.Page) -> None:
    page.title = "Flet Components"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=COLORS.accent)
    page.bgcolor = COLORS.background
    page.padding = 0
    page.render(App)


if __name__ == "__main__":
    ft.run(main)
