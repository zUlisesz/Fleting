"""Botón atómico para acciones representadas por un icono."""

from collections.abc import Callable

import flet as ft

from theme import COLORS


def shadcn_icon_button(
    icon: ft.IconData,
    *,
    on_click: Callable[..., None] | None = None,
    tooltip: str | None = None,
    selected: bool = False,
    size: int | float = 44,
    icon_size: int | float = 22,
    inverse: bool = False,
) -> ft.IconButton:
    """Crea un botón cuadrado de icono con estados discretos."""

    foreground = COLORS.surface if inverse else COLORS.text
    background = COLORS.text if inverse else COLORS.surface
    hover = COLORS.text_secondary if inverse else COLORS.background

    return ft.IconButton(
        icon=icon,
        icon_color=foreground,
        icon_size=icon_size,
        selected=selected,
        tooltip=tooltip,
        on_click=on_click,
        width=size,
        height=size,
        style=ft.ButtonStyle(
            bgcolor={
                ft.ControlState.DEFAULT: background,
                ft.ControlState.HOVERED: hover,
                ft.ControlState.SELECTED: hover,
            },
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=8,
        ),
    )

