import flet as ft
from back import Shell

def main(page: ft.Page):
    page.horizontal_alignment =ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 1200
    page.window.height = 800
    page.window.alignment = ft.Alignment.CENTER
    page.padding = 24

    zsh = Shell()

    def selectDir(e) :
        namedir = e.control.content.controls[1].value
        zsh.cd( namedir)
        updateSideBar()

    def makecard( name: str) -> ft.Card:
        return ft.Card(
            shadow_color=ft.Colors.ON_SURFACE_VARIANT,
            elevation= 10,
            content=ft.Container(
                on_click= selectDir,
                ink= True,
                width= 220,
                padding=10,
                border_radius=8,
                content= ft.Row(
                    controls= [
                        ft.Icon( icon= ft.Icons.BOOK_SHARP),
                        ft.Text(
                            font_family= 'Courier',
                            value= name
                        ),
                    ]
                )
            ),
        )

    dirStack = ft.Column(
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
        spacing= 4,
        controls= [
            makecard(dir) for dir in zsh.lsdir()
        ]
    )

    def updateSideBar():  
        dirStack.controls.clear()
        for dir in zsh.lsdir():
            dirStack.controls.append( makecard(dir))

        page.update()
    

    sidebar = ft.Container(
        width= 300,
        alignment= ft.Alignment.CENTER,
        height= 700,
        border_radius=10 ,
        padding= 20, 
        bgcolor= ft.Colors.TEAL_200,
        content= ft.Column(
            scroll=ft.ScrollMode.HIDDEN, 
            controls=[
                ft.Text(
                    value= zsh.cwd
                ),
                dirStack
            ]
        )
    )

    topbar = ft.Container(
        height= 120,
        width= 760, 
        alignment= ft.Alignment.CENTER , 
        content= ft.Text(
            'GESTOR DE ARCHIVOS',
            font_family= 'Courier',
            size= 30 ,
            weight= ft.FontWeight.BOLD
        ), 
        bgcolor= ft.Colors.TEAL_300,
        border_radius= 10 
    )

    body = ft.Container(
        width= 760,
        height= 540, 
        padding= 24,
        bgcolor= ft.Colors.LIGHT_BLUE_100,
        content= ft.Text(
            zsh.cwd
        ),
        border_radius= 10,
    )

    layout = ft.Container(
        width= 1120,
        height= 720,
        bgcolor= ft.Colors.TEAL,
        border_radius= 12,
        padding= 20,

        content= ft.Row(
            controls= [
                sidebar,
                ft.Column(
                    controls=[
                        topbar,
                        body
                    ],
                    spacing=20
                )
            ],
            spacing= 20 ,
        )
    )

    page.add(
        layout
    )

ft.run(main)