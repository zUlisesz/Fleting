from model import data 
import flet as ft

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    page.add(
        ft.Container(
            alignment= ft.Alignment.CENTER,
            padding= 20 ,
            content= ft.Image(
                src='/woman_6.png',
                width=100,
                height=140,
                fit=ft.BoxFit.COVER,
            )
        ),
        ft.Text('Avatar preview')
    )

ft.run(main, assets_dir="assets")