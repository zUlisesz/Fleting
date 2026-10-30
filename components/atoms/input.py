"""Campos de texto atómicos con apariencia inspirada en shadcn/ui."""

from collections.abc import Callable

import flet as ft

from theme import COLORS


def _input_border(color: str) -> ft.OutlineInputBorder:
    """Construye un borde de entrada para un estado interactivo."""

    return ft.OutlineInputBorder(
        side=ft.BorderSide(width=1, color=color),
        border_radius=ft.BorderRadius.all(8),
    )


def shadcn_input(
    label: str,
    *,
    hint_text: str | None = None,
    value: str = "",
    on_change: Callable[..., None] | None = None,
    width: int | float | None = 320,
) -> ft.TextField:
    """Crea un campo con estados default, hover y focus."""

    return ft.TextField(
        label=label,
        hint_text=hint_text,
        value=value,
        width=width,
        on_change=on_change,
        color=COLORS.text,
        label_style=ft.TextStyle(color=COLORS.text_secondary),
        hint_style=ft.TextStyle(color=COLORS.placeholder),
        cursor_color=COLORS.text,
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=14),
        border={
            ft.ControlState.DEFAULT: _input_border(COLORS.border),
            ft.ControlState.HOVERED: _input_border(COLORS.muted),
            ft.ControlState.FOCUSED: _input_border(COLORS.text),
        },
    )

