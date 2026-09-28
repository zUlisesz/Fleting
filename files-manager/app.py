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

    def makecard( name: str, type : str = 's' ) -> ft.Card:

        stype = ft.Container(
            ink= True,
            width= 220 if type == 's' else 700,
            padding=10,
            border_radius=8,
            on_click= selectDir,
            content= ft.Row(
                controls= [
                    ft.Icon( icon= ft.Icons.BOOK_SHARP),
                    ft.Text(
                        font_family= 'Courier',
                        value= name
                    ),
                ]
            )
        )
        if type == 's':
            return ft.Card(
                shadow_color=ft.Colors.ON_SURFACE_VARIANT,
                elevation= 10,
                content= stype
            ) 

        return ft.Card(
            shadow_color= ft.Colors.ON_SURFACE_VARIANT,
            elevation= 10 ,
            content= ft.Container(
                width= 700,
                padding=10,
                bgcolor= ft.Colors.LIME_100,
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
            )
        )


    dirStack = ft.Column(
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
        spacing= 4,
        controls= [
            makecard(dir) for dir in zsh.lsdir()
        ]
    )

    innerdirstack = ft.Column(
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
        controls=[],
        scroll = ft.ScrollMode.HIDDEN  ,
        spacing= 4
    )

    def updateSideBar():  

        dirStack.controls.clear()
        innerdirstack.controls.clear()

        """short cards"""
        for dir in zsh.lsdir():
            dirStack.controls.append( makecard(dir, 's'))

        innerdirstack.controls.append(
            makecard('../', 's')
        )
        innerdirstack.controls[0].width = 710 #type: ignore
        for element in zsh.ls():
            innerdirstack.controls.append( makecard(element, 'l'))

        pwd.value = zsh.cwd

        page.update()
    
    pwd = ft.Text(
        zsh.cwd
    )

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
                dirStack
            ]
        )
    )

    topbar = ft.Container(
        height= 120,
        width= 760, 
        alignment= ft.Alignment.CENTER , 
        content= ft.Column(
            controls = [
                ft.Text(
                    'GESTOR DE ARCHIVOS',
                    font_family= 'Courier',
                    size= 30 ,
                    weight= ft.FontWeight.BOLD
                ),
                pwd
            ]

        ), 
        bgcolor= ft.Colors.TEAL_300,
        border_radius= 10 
    )

    body = ft.Container(
        width= 760,
        height= 540, 
        padding= 24,
        alignment= ft.Alignment.CENTER_LEFT,
        bgcolor= ft.Colors.LIGHT_BLUE_100,
        content= innerdirstack,
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