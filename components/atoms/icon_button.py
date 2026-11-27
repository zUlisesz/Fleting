"""Botón cuadrado que solo muestra un icono."""

from collections.abc import Callable

import flet as ft

from ..theme import COLORS


@ft.component
def IconButton(
    icon: ft.IconData,
    *,
    on_click: Callable[..., None] | None = None,
    tooltip: str | None = None,
    selected: bool = False,
    size: int | float = 44,
    icon_size: int | float = 22,
    inverse: bool = False,
) -> ft.Control:
    """Botón de icono. ``inverse=True`` lo muestra oscuro sobre fondo claro."""
    foreground = COLORS.surface if inverse else COLORS.text
    background = COLORS.text if inverse else COLORS.surface
    hover = COLORS.text_secondary if inverse else COLORS.background
    state = ft.ControlState

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
                state.DEFAULT: background,
                state.HOVERED: hover,
                state.SELECTED: hover,
            },
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=8,
        ),
    )
