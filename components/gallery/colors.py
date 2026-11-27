"""Explorador de los colores de ``ft.Colors``."""

import flet as ft

from ._catalog import CatalogBrowser

COLORS_CATALOG = tuple(ft.Colors)


@ft.component
def ColorTile(color: ft.Colors) -> ft.Control:
    """Muestra una muestra de color y su nombre."""
    return ft.Container(
        height=110,
        bgcolor=color,
        border=ft.Border.all(1, ft.Colors.OUTLINE),
        border_radius=12,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        alignment=ft.Alignment.BOTTOM_CENTER,
        content=ft.Container(
            bgcolor=ft.Colors.with_opacity(0.88, ft.Colors.WHITE),
            padding=4,
            content=ft.Text(
                f"ft.Colors.{color.name}",
                size=10,
                color=ft.Colors.BLACK,
                selectable=True,
                text_align=ft.TextAlign.CENTER,
            ),
        ),
    )


@ft.component
def ColorsGallery() -> ft.Control:
    return CatalogBrowser(
        COLORS_CATALOG,
        lambda color: ColorTile(color, key=color.name),
        noun="colores",
        hint_text="blue, amber, grey…",
    )
