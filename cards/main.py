import flet as ft

try:
    from .model import data
except ImportError:  # Permite ejecutar: python main.py desde esta carpeta.
    from model import data

def main(page: ft.Page):
    page.window.alignment = ft.Alignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 1200

    def _stat_block(title: str, phone: str, address: str, avatar: str) -> ft.Control:
        return ft.Container(
            col={"xs": 12, "sm": 6, "lg": 3},
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
                    ft.Text(phone, size=12, text_align=ft.TextAlign.CENTER),
                    ft.Text(
                        address,
                        size=11,
                        max_lines=2,
                        overflow=ft.TextOverflow.ELLIPSIS,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        )

    page.add(
        ft.SafeArea( 
            content=ft.ResponsiveRow(
                controls=[
                    _stat_block(user["name"], user["phone"], user["address"], user["avatar"])
                    for user in data
                ],
                columns=12,
                spacing=16,
                run_spacing=16,
            )
        )
    )

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
