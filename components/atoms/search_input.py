"""Campo de búsqueda: un ``TextInput`` con icono de lupa."""

from collections.abc import Callable

import flet as ft

from .text_input import TextInput


@ft.component
def SearchInput(
    *,
    value: str = "",
    hint_text: str = "Search",
    on_change: Callable[..., None] | None = None,
    width: int | float = 360,
) -> ft.Control:
    """Campo de búsqueda controlado (igual que ``TextInput``)."""
    return TextInput(
        value=value,
        hint_text=hint_text,
        prefix_icon=ft.Icons.SEARCH,
        on_change=on_change,
        width=width,
    )
