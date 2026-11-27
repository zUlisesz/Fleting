"""Punto de entrada de Balance.
    python3 -m finanzas.main     # desde la carpeta que contiene `finanzas/`
"""

import sqlite3
import flet as ft

from .app import App
from .repositorio import Repositorio, ruta_por_defecto


def main(page: ft.Page) -> None:
    page.title = "Balance · Flujo de efectivo"
    page.padding = 24
    page.scroll = ft.ScrollMode.AUTO
    page.window.width = 880
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.TEAL)
    page.theme_mode = ft.ThemeMode.LIGHT

    try:
        repo = Repositorio(ruta_por_defecto())
    except (OSError, sqlite3.Error) as error:
        page.add(ft.Text(f"No se pudo abrir el almacenamiento: {error}"))
        return
    page.render(App, repo)


if __name__ == "__main__":
    ft.run(main)
