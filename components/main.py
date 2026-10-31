"""Demo mínima con botones, búsqueda y shimmer."""

import flet as ft

from atoms import search_input
from gallery import button_gallery, shimmer_gallery
from theme import COLORS


def main(page: ft.Page) -> None:
    """Presenta únicamente los componentes activos del catálogo."""

    page.title = "Flet Elementals · Buttons and Search"
    page.bgcolor = "#0A0A0A"
    page.padding = 0
    page.theme = ft.Theme(color_scheme_seed=COLORS.accent)
    page.scroll = ft.ScrollMode.AUTO

    search = search_input(hint_text="Search components", width=420)
    result = ft.Text("", color="#E1E1EA", size=14)

    def search_change(_: ft.ControlEvent) -> None:
        query = search.value.strip()
        result.value = f"Searching for: {query}" if query else ""
        result.update()

    search.on_change = search_change

    page.add(
        ft.Container(
            padding=ft.Padding.symmetric(horizontal=32, vertical=28),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Flet Elementals",
                        color=COLORS.surface,
                        size=32,
                        weight=ft.FontWeight.W_700,
                    ),
                    ft.Text(
                        "Buttons, search input y shimmer reutilizables.",
                        color="#A1A1AA",
                        size=16,
                    ),
                    ft.Divider(color=COLORS.border, thickness=1),
                    ft.Container(
                        padding=24,
                        border=ft.Border.all(1, COLORS.border),
                        border_radius=16,
                        content=ft.Column(
                            controls=[
                                ft.Text("Search input", color=COLORS.surface, size=20),
                                search,
                                result,
                            ],
                            spacing=12,
                        ),
                    ),
                    ft.Text("Button gallery", color=COLORS.surface, size=22, weight=ft.FontWeight.W_600),
                    button_gallery(),
                    ft.Text("Shimmer gallery", color=COLORS.surface, size=22, weight=ft.FontWeight.W_600),
                    shimmer_gallery(),
                ],
                spacing=24,
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
