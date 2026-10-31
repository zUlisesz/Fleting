"""Search input atómico con icono de búsqueda."""

from collections.abc import Callable

import flet as ft

from atoms.input import shadcn_input


def search_input(
    *,
    hint_text: str = "Search",
    value: str = "",
    on_change: Callable[..., None] | None = None,
    width: int | float = 360,
) -> ft.TextField:
    """Crea un campo de búsqueda reutilizable con icono integrado."""

    return shadcn_input(
        "",
        hint_text=hint_text,
        value=value,
        prefix_icon=ft.Icons.SEARCH,
        on_change=on_change,
        width=width,
    )
