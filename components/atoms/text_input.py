"""Campos de texto atómicos con apariencia inspirada en shadcn/ui."""

from collections.abc import Callable

import flet as ft

try:
    from ..theme import COLORS
except ImportError:  # Permite importar desde components/main.py.
    from theme import COLORS


def shadcn_input(
    label: str,
    *,
    hint_text: str | None = None,
    value: str = "",
    password: bool = False,
    can_reveal_password: bool = False,
    outlined: bool = True,
    prefix_icon: ft.IconData | None = None,
    on_change: Callable[..., None] | None = None,
    width: int | float | None = 320,
) -> ft.TextField:
    """Crea un campo con estados default y focus."""

    return ft.TextField(
        label=label,
        hint_text=hint_text,
        value=value,
        password=password,
        can_reveal_password=can_reveal_password,
        prefix_icon=prefix_icon,
        width=width,
        on_change=on_change,
        color=COLORS.text,
        label_style=ft.TextStyle(color=COLORS.text_secondary),
        hint_style=ft.TextStyle(color=COLORS.placeholder),
        cursor_color=COLORS.text,
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=14),
        border=ft.InputBorder.OUTLINE if outlined else ft.InputBorder.NONE,
        border_width=1,
        border_radius=ft.BorderRadius.all(8),
        border_color=COLORS.border,
        focused_border_width=1,
        focused_border_color=COLORS.text,
    )

