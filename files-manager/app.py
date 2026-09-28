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

    dirStack = ft.Column(
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text( 
                value = zsh.cwd
            ),
            ft.Divider(color= ft.Colors.BLACK)
        ],
        scroll= ft.ScrollMode.AUTO,
        spacing= 4
    )

    def selectDir(e) :
        namedir = e.control.content.controls[1].value
        print(namedir, zsh.cwd)
        zsh.cd( namedir)
        print(zsh.cwd, zsh.lsdir())
        updateSideBar()
        page.update()

    def makecard( name: str) -> ft.Card:
        return ft.Card(
            shadow_color=ft.Colors.ON_SURFACE_VARIANT,
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

    def updateSideBar():   
        lista = zsh.lsdir()
        for dir in lista:
            dirStack.controls.append( makecard(dir))

        page.update()
    
    updateSideBar()

    sidebar = ft.Container(
        width= 260,
        height= 700,
        border_radius=10 ,
        padding= 20, 
        bgcolor= ft.Colors.TEAL_200,
        content= dirStack
    )

    topbar = ft.Container(
        height= 120,
        width= 800, 
        bgcolor= ft.Colors.TEAL_300,
        border_radius= 10 
    )

    body = ft.Container(
        width= 800,
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