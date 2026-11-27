"""Explorador paginado y filtrable de catálogos grandes (iconos, colores)."""

from collections.abc import Callable, Sequence
from enum import Enum
from typing import TypeVar

import flet as ft

from ..atoms import Button, SearchInput
from ._layout import TILE_COLS, ResponsiveGrid

PAGE_SIZE = 120
M = TypeVar("M", bound=Enum)


def filter_members(members: Sequence[M], query: str) -> list[M]:
    """Miembros cuyo nombre contiene ``query`` (sin distinguir mayúsculas)."""
    term = query.strip().casefold()
    return [m for m in members if term in m.name.casefold()]


def page_count(total: int, page_size: int = PAGE_SIZE) -> int:
    """Número de páginas necesarias (siempre al menos una)."""
    return max(1, -(-total // page_size))


def page_slice(items: Sequence[M], page: int, page_size: int = PAGE_SIZE) -> Sequence[M]:
    """Elementos de la página ``page`` (base 0)."""
    start = page * page_size
    return items[start : start + page_size]


@ft.component
def CatalogBrowser(
    members: Sequence[M],
    tile: Callable[[M], ft.Control],
    *,
    noun: str,
    hint_text: str = "Buscar…",
) -> ft.Control:
    """Cuadrícula con búsqueda por nombre y botones Anterior/Siguiente.

    ``tile`` recibe un miembro y devuelve su control; ``noun`` se usa en el
    contador (p. ej. ``"iconos"``).
    """
    query, set_query = ft.use_state("")
    page, set_page = ft.use_state(0)

    matches = ft.use_memo(lambda: filter_members(members, query), [members, query])
    pages = page_count(len(matches))
    current = min(page, pages - 1)

    def on_search(e: ft.Event) -> None:
        set_query(e.control.value)
        set_page(0)

    return ft.Column(
        spacing=12,
        controls=[
            SearchInput(value=query, hint_text=hint_text, on_change=on_search, width=420),
            ft.Text(f"{len(matches):,} {noun} · página {current + 1} de {pages}"),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    Button(
                        "Anterior",
                        variant="outline",
                        icon=ft.Icons.CHEVRON_LEFT,
                        disabled=current == 0,
                        on_click=lambda _: set_page(current - 1),
                    ),
                    Button(
                        "Siguiente",
                        variant="outline",
                        icon=ft.Icons.CHEVRON_RIGHT,
                        disabled=current >= pages - 1,
                        on_click=lambda _: set_page(current + 1),
                    ),
                ],
            ),
            ResponsiveGrid(
                [tile(m) for m in page_slice(matches, current)],
                cols=TILE_COLS,
                spacing=10,
            ),
        ],
    )
