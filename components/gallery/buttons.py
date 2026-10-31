"""Galería reutilizable de botones con iconos."""

import flet as ft

from atoms import shadcn_button, shadcn_icon_button, surface


def button_gallery() -> ft.ResponsiveRow:
    """Recrea la galería de botones conservando el átomo de botón."""

    actions = [
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
    ]
    cards: list[ft.Control] = []
    for label, icon in actions:
        cards.append(
            ft.Container(
                col={"xs": 12, "sm": 6, "md": 4},
                content=surface(
                    ft.Row(
                        controls=[shadcn_button(label, icon=icon)],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=24,
                    radius=12,
                    height=150,
                ),
            )
        )

    cards.extend(
        [
            ft.Container(
                col={"xs": 12, "sm": 6, "md": 4},
                content=surface(
                    ft.Row(
                        controls=[
                            shadcn_icon_button(ft.Icons.NIGHTLIGHT_OUTLINED),
                            shadcn_icon_button(ft.Icons.CONTENT_COPY, inverse=True, size=48),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=94,
                    ),
                    padding=24,
                    radius=12,
                    height=150,
                ),
            ),
            ft.Container(
                col={"xs": 12, "sm": 6, "md": 4},
                content=surface(
                    ft.Row(
                        controls=[shadcn_icon_button(ft.Icons.VISIBILITY_OUTLINED)],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=24,
                    radius=12,
                    height=150,
                ),
            ),
        ]
    )
    return ft.ResponsiveRow(controls=cards, spacing=16, run_spacing=16)
