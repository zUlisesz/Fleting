"""Demostración de los átomos ``Button`` e ``IconButton``."""

import flet as ft

from ..atoms import Button, IconButton, Surface
from ._layout import CARD_COLS, ResponsiveGrid

ACTIONS: tuple[tuple[str, ft.IconData], ...] = (
    ("Send", ft.Icons.SEND),
    ("Refresh", ft.Icons.REFRESH),
    ("More", ft.Icons.MORE_HORIZ),
    ("Home", ft.Icons.HOME_OUTLINED),
    ("Profile", ft.Icons.PERSON_OUTLINE),
    ("Message", ft.Icons.CHAT_BUBBLE_OUTLINE),
    ("Theme", ft.Icons.NIGHTLIGHT_OUTLINED),
    ("Preview", ft.Icons.VISIBILITY_OUTLINED),
    ("Visit Site", ft.Icons.OPEN_IN_NEW),
    ("Next", ft.Icons.CHEVRON_RIGHT),
    ("Confirm", ft.Icons.CHECK),
    ("Lock", ft.Icons.LOCK_OUTLINE),
    ("Filter", ft.Icons.FILTER_ALT_OUTLINED),
    ("Download", ft.Icons.DOWNLOAD),
    ("Upload", ft.Icons.UPLOAD),
    ("Share", ft.Icons.SHARE),
    ("Settings", ft.Icons.SETTINGS_OUTLINED),
    ("Help", ft.Icons.HELP_OUTLINE),
    ("Info", ft.Icons.INFO_OUTLINE),
    ("Alert", ft.Icons.ERROR_OUTLINE),
    ("Menu", ft.Icons.MENU),
    ("Cart", ft.Icons.SHOPPING_CART_OUTLINED),
    ("Favorite", ft.Icons.FAVORITE_BORDER),
    ("Rate", ft.Icons.STAR_BORDER),
)


def _centered(*controls: ft.Control) -> ft.Control:
    return Surface(
        ft.Row(controls=list(controls), alignment=ft.MainAxisAlignment.CENTER),
        radius=12,
        height=110,
    )


@ft.component
def ButtonsGallery() -> ft.Control:
    last_action, set_last_action = ft.use_state("ninguna")

    def pressed(name: str):
        return lambda _: set_last_action(name)

    cells = [
        _centered(Button(label, icon=icon, on_click=pressed(label)))
        for label, icon in ACTIONS
    ]
    cells += [
        _centered(
            Button("Outline", variant="outline", on_click=pressed("Outline")),
            Button("Disabled", disabled=True),
        ),
        _centered(
            IconButton(ft.Icons.NIGHTLIGHT_OUTLINED, on_click=pressed("Theme icon")),
            IconButton(
                ft.Icons.CONTENT_COPY, inverse=True, size=48, on_click=pressed("Copy")
            ),
        ),
    ]
    return ft.Column(
        spacing=16,
        controls=[
            ft.Text(f"Última acción: {last_action}", color=ft.Colors.ON_SURFACE_VARIANT),
            ResponsiveGrid(cells, cols=CARD_COLS),
        ],
    )
