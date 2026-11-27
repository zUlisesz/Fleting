"""Campo de texto con estados default y focus."""

from collections.abc import Callable

import flet as ft

from ..theme import COLORS


@ft.component
def TextInput(
    label: str = "",
    *,
    value: str = "",
    hint_text: str | None = None,
    password: bool = False,
    can_reveal_password: bool = False,
    outlined: bool = True,
    prefix_icon: ft.IconData | None = None,
    on_change: Callable[..., None] | None = None,
    width: int | float | None = 320,
) -> ft.Control:
    """Campo de texto controlado: el valor mostrado es siempre ``value``.

    Guarda el texto con ``ft.use_state`` en el componente que lo usa:

    >>> text, set_text = ft.use_state("")
    >>> TextInput("Nombre", value=text, on_change=lambda e: set_text(e.control.value))
    """
    return ft.TextField(
        label=label or None,
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
        border=ft.OutlineInputBorder() if outlined else ft.NoInputBorder(),
        border_width=1,
        border_radius=8,
        border_color=COLORS.border,
        focused_border_width=1,
        focused_border_color=COLORS.text,
    )
