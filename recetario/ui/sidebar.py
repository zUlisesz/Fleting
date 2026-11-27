"""Barra lateral: buscador y lista de recetas."""

from collections.abc import Callable

import flet as ft

from domain import Recipe

from . import theme
from .widgets import EmptyHint


@ft.component
def RecipeItem(recipe: Recipe, *, selected: bool, on_select: Callable[[str], None]) -> ft.Control:
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=14, vertical=12),
        border_radius=12,
        bgcolor=theme.ACCENT_SOFT if selected else ft.Colors.WHITE,
        border=ft.Border.all(
            1.5 if selected else 1, theme.ACCENT if selected else theme.BORDER
        ),
        ink=True,
        on_click=lambda _: on_select(recipe.id),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=10,
                    expand=True,
                    controls=[
                        ft.Icon(
                            ft.Icons.MENU_BOOK_ROUNDED,
                            size=20,
                            color=theme.ACCENT_DARK if selected else theme.MUTED,
                        ),
                        ft.Text(
                            recipe.title,
                            size=14,
                            expand=True,
                            weight=ft.FontWeight.W_600 if selected else ft.FontWeight.W_500,
                            color=ft.Colors.TEAL_900 if selected else theme.TEXT,
                        ),
                    ],
                ),
                ft.Icon(
                    ft.Icons.CHEVRON_RIGHT_ROUNDED,
                    size=18,
                    color=theme.ACCENT if selected else ft.Colors.GREY_400,
                ),
            ],
        ),
    )


@ft.component
def Sidebar(
    recipes: list[Recipe],
    *,
    selected_id: str | None,
    query: str,
    on_query: Callable[[str], None],
    on_select: Callable[[str], None],
    on_new: Callable[[], None],
) -> ft.Control:
    """``recipes`` ya viene filtrada por ``query``."""
    if recipes:
        items = [
            RecipeItem(r, selected=r.id == selected_id, on_select=on_select, key=r.id)
            for r in recipes
        ]
    else:
        items = [
            EmptyHint(
                "No se encontraron recetas" if query.strip() else "Aún no tienes recetas registradas"
            )
        ]

    return ft.Container(
        width=theme.SIDEBAR_WIDTH,
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.only(right=ft.BorderSide(1, ft.Colors.GREY_300)),
        padding=ft.Padding.symmetric(horizontal=18, vertical=20),
        content=ft.Column(
            spacing=14,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            spacing=8,
                            controls=[
                                ft.Icon(ft.Icons.BOOK_ROUNDED, color=theme.ACCENT_DARK, size=24),
                                ft.Text(
                                    "Recetario",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=theme.TEXT_STRONG,
                                ),
                            ],
                        ),
                        ft.IconButton(
                            icon=ft.Icons.ADD_ROUNDED,
                            icon_color=ft.Colors.WHITE,
                            bgcolor=theme.ACCENT_DARK,
                            tooltip="Nueva receta",
                            on_click=lambda _: on_new(),
                        ),
                    ],
                ),
                ft.TextField(
                    value=query,
                    hint_text="Buscar recetas...",
                    prefix_icon=ft.Icons.SEARCH,
                    dense=True,
                    border_radius=12,
                    bgcolor=ft.Colors.WHITE,
                    border_color=ft.Colors.GREY_300,
                    on_change=lambda e: on_query(e.control.value),
                ),
                ft.Text("MIS RECETAS", size=11, weight=ft.FontWeight.BOLD, color=theme.FAINT),
                ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO, expand=True, controls=items),
            ],
        ),
    )
