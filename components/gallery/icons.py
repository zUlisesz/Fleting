"""Explorador de los iconos de ``ft.Icons``."""

import flet as ft

from ._catalog import CatalogBrowser

ICONS = tuple(ft.Icons)


@ft.component
def IconTile(icon: ft.Icons) -> ft.Control:
    """Muestra el glifo y cómo referenciarlo en código."""
    return ft.Container(
        height=100,
        padding=10,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=12,
        content=ft.Column(
            spacing=6,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(icon, size=26),
                ft.Text(
                    f"ft.Icons.{icon.name}",
                    size=9,
                    selectable=True,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        ),
    )


@ft.component
def IconsGallery() -> ft.Control:
    return CatalogBrowser(
        ICONS,
        lambda icon: IconTile(icon, key=icon.name),
        noun="iconos",
        hint_text="ADD, home, arrow…",
    )
