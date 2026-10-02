import flet as ft
from model import data 

def main(page: ft.Page):
    page.window.alignment = ft.Alignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 1200

    def _stat_block(title: str, subtitle: str, avatar: str) -> ft.Control:
        return ft.Container(
            width=200,
            padding=ft.Padding.all(20),
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            border_radius=ft.BorderRadius.all(24),
            content=ft.Column(
                spacing=16,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        alignment=ft.Alignment.CENTER,
                        content=ft.Image(
                            src=avatar,
                            width=100,
                            height=140,
                            fit=ft.BoxFit.COVER,
                            repeat=ft.ImageRepeat.NO_REPEAT,
                            border_radius=ft.BorderRadius.all(10),
                        ),
                    ),
                    ft.Text(title, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER),
                    ft.Text(subtitle, size=12, text_align=ft.TextAlign.CENTER),
                ],
            ),
        )

    page.add(
        ft.SafeArea( 
            content=ft.Row(
                controls=[
                    _stat_block(user['name'], user['phone'], user['avatar'])
                    for user in data
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
    )

ft.run(main, assets_dir="assets")