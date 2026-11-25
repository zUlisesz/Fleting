"""Punto de compatibilidad para los controles elementales.

Los controles viven en ``atoms/`` para facilitar su reutilización. Este
módulo conserva los imports anteriores y permite seguir ejecutando la demo
con ``flet run elementals.py``.
"""

import flet as ft

from atoms import search_input, shadcn_button, shadcn_icon_button, shadcn_input, surface
from main import main

__all__ = [
    "main",
    "search_input",
    "shadcn_button",
    "shadcn_icon_button",
    "shadcn_input",
    "surface",
]


if __name__ == "__main__":
    ft.run(main)
