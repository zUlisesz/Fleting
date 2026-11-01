"""Galería simple de todos los colores disponibles en Flet."""

import flet as ft


def color_gallery() -> ft.Row:
    """Muestra una muestra cuadrada y el nombre de cada miembro de ft.Colors."""

    return ft.Row(
        wrap=True,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=16,
        run_spacing=16,
        controls=[
            ft.Container(
                width=132,
                height=132,
                bgcolor=color,
                border=ft.Border.all(1, ft.Colors.OUTLINE),
                border_radius=12,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                alignment=ft.Alignment.BOTTOM_CENTER,
                content=ft.Container(
                    bgcolor=ft.Colors.with_opacity(0.88, ft.Colors.WHITE),
                    border_radius=8,
                    padding=4,
                    content=ft.Text(
                        f"ft.Colors.{color.name}",
                        size=10,
                        color=ft.Colors.BLACK,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ),
            )
            for color in ft.Colors
        ],
    )


def main(page: ft.Page) -> None:
    """Abre la galería como una aplicación independiente."""

    page.title = "Flet Colors"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 16
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.add(ft.Text("ft.Colors", size=24, weight=ft.FontWeight.BOLD), color_gallery())


if __name__ == "__main__":
    ft.run(main)
