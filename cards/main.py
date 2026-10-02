import flet as ft
from model import data 

def main(page: ft.Page):
    page.window.alignment = ft.Alignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 920

    def _stat_block(title: str, subtitle: str) -> ft.Control:

        def metric(width: int, height: int = 14,) -> ft.Control:
            return ft.Container(
                width=width,
                height=height,
                bgcolor=ft.Colors.WHITE,
                opacity=0.6,
                border_radius=ft.BorderRadius.all(height),
            )

        return ft.Container(
            width=200,
            padding=ft.Padding.all(20),
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            border_radius=ft.BorderRadius.all(24),
            content=ft.Column(
                spacing=16,
                controls=[
                    ft.Container(
                        width= 200,
                        height= 120,
                        bgcolor= ft.Colors.AMBER,
                        border_radius= 8
                    ),
                    ft.Container(
                        border_radius=ft.BorderRadius.all(16),
                        bgcolor=ft.Colors.WHITE,
                        opacity=0.35,
                    ),
                    ft.Text(title, weight=ft.FontWeight.W_600),
                    ft.Text(subtitle, size=12),
                ],
            ),
        )


    accent = ft.LinearGradient(
        begin=ft.Alignment(-1.0, -0.5),
        end=ft.Alignment(1.0, 0.5),
        colors=[
            ft.Colors.PURPLE,
            ft.Colors.PURPLE,
            ft.Colors.AMBER_200,
            ft.Colors.PURPLE,
            ft.Colors.PURPLE,
        ],
        stops=[0.0, 0.35, 0.5, 0.65, 1.0],
    )


    page.add(
        ft.SafeArea( 
            content= ft.Row(
                controls = [
                    ft.Shimmer(
                        gradient=accent,
                        direction=ft.ShimmerDirection.TTB,
                        period=2200,
                        content=_stat_block(user['name'], user['phone']),
                    )
                    for user in data
                ],
                alignment= ft.MainAxisAlignment.CENTER,
                vertical_alignment= ft.CrossAxisAlignment.CENTER

            )
        )
    )

ft.run( main)