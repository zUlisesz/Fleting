from model import Cajero
import flet_audio as fv
from typing import Callable
import flet as ft

def main( page : ft.Page):
    page.window.alignment = ft.Alignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = 720
    page.padding = 40
    page.title = 'ATM with FLET'

    audio = fv.Audio(
        src= '/audio/click.wav',
        volume= 0.20, 
        release_mode= fv.ReleaseMode.STOP
    )

    succes = fv.Audio(
        src ='/audio/success.wav',
        volume= 0.4,
        release_mode= fv.ReleaseMode.STOP
    )

    async def sonido_numero():
        await audio.play()

    async def sonido_success():
        await succes.play()

    bbva = Cajero()

    def generar_billetes():
        monto = int ( ventana.content.value )
        billetes.controls = [
            billete_control(f'{billete}')
            for billete in bbva.entregar_dinero(monto)
        ]

        texto, stat =  bbva.mesaje_retiro(monto)
        status.value = texto
        status.color = ft.Colors.PINK_ACCENT_700
        if stat:
            status.color = ft.Colors.with_opacity(0.8, ft.Colors.CYAN_ACCENT)

    async def click_numero(e):
        data = e.control.content.value
        ventana.content.value += data 
        await sonido_numero()

    def click_borrar(e):
        data = ventana.content.value
        ventana.content.value = ''.join( list(data)[:-1])

    async def click_enter(e):
        generar_billetes()
        ventana.content.value = ''
        await sonido_success()

    def billete_control(value : str) -> ft.Card:
        return ft.Card(
            elevation= 10 ,
            shadow_color= ft.Colors.LIME,
            content= ft.Container(
                width= 120,
                height= 50,
                alignment= ft.Alignment.CENTER,
                border_radius= 8,
                shadow= ft.BoxShadow(
                    blur_radius= 12,
                    color= ft.Colors.with_opacity( 0.2 , ft.Colors.GREEN_ACCENT_400)
                ),
                bgcolor= ft.Colors.GREEN_900,
                content= ft.Container(
                    width= 104,
                    height= 40,
                    padding= ft.Padding.only( left= 20 , right= 20 ),
                    alignment= ft.Alignment.CENTER,
                    border_radius= 6,
                    bgcolor= ft.Colors.GREEN_ACCENT_400,
                    shadow= ft.BoxShadow(
                        blur_radius= 8,
                        color= ft.Colors.with_opacity( 0.2 , ft.Colors.GREEN_ACCENT_700)
                    ),
                    content= ft.Row(
                        alignment= ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls= [
                            ft.Icon( 
                                icon= ft.Icons.MONETIZATION_ON_OUTLINED, 
                                size= 18,
                                color= ft.Colors.AMBER_ACCENT_700
                            ),
                            ft.Text(
                                value, 
                                weight= ft.FontWeight.BOLD,
                                color= ft.Colors.GREEN_900
                            )
                        ]
                    )
                )
            )
        )

    billetes =ft.Column(
        spacing= 0, 
        height= 470,
        wrap= True,
        alignment= ft.MainAxisAlignment.START,
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
        controls= []
    )

    def generarControles():
        columna = ft.Column(
            alignment= ft.MainAxisAlignment.CENTER ,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER
        )
        valor = 1 
        for _ in range(3):
            columna.controls.append(
                row := ft.Row(
                    alignment= ft.MainAxisAlignment.CENTER
                )
            )
            for _ in range(3):
                row.controls.append(
                    boton_control( f'{valor}', click_numero)
                )
                valor += 1

        columna.controls.append(
            ft.Row(
                alignment= ft.MainAxisAlignment.CENTER,
                controls=[
                    boton_control('0', click_numero),
                    boton_control('BORRAR', click_borrar),
                    boton_control('ENTER',click_enter)
                ]
            )
        )

        return columna

    def boton_control( value : str, evento: Callable):
        return ft.Container(
            height= 36,
            width= 74,
            alignment= ft.Alignment.CENTER,
            content= ft.Text(
                value,
                weight= ft.FontWeight.BOLD
            ),
            ink= True,
            ink_color= ft.Colors.CYAN_700,
            on_click= evento,
            border_radius= 6,
            bgcolor= ft.Colors.GREY_700
        )

    ventana = ft.Container(
        width= 240 ,
        height= 56,
        padding= 10 ,
        bgcolor= ft.Colors.WHITE,
        border_radius= 8,
        shadow= ft.BoxShadow(
            blur_radius= 20,
            color= ft.Colors.with_opacity( 0.4, ft.Colors.CYAN_ACCENT)
        ),
        content= ft.Text(
            value = '',
            size = 20,
            weight= ft.FontWeight.W_800,
            color = ft.Colors.BLACK,
            text_align= ft.TextAlign.END
        ),
        alignment= ft.Alignment.CENTER_RIGHT
    )

    maquina = ft.Card(
        content= ft.Container(
            border_radius= 10 ,
            height= 440,
            padding= 20,
            width= 300,
            alignment= ft.Alignment.TOP_CENTER,
            bgcolor= ft.Colors.GREY_900, 
            border=ft.Border.all(1, '#3D4251'),
            shadow=ft.BoxShadow(
                blur_radius=20,
                color=ft.Colors.with_opacity(0.8, '#00E8C6')
            ),
            content= ft.Column(
                spacing= 20, 
                alignment= ft.MainAxisAlignment.CENTER,
                horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                controls = [
                    ft.Text(
                        value= 'BBVA',
                        size= 30 ,
                        weight= ft.FontWeight.BOLD,
                        color = ft.Colors.CYAN_500
                    ),
                    ventana,
                    status := ft.Text(),
                    generarControles()
                ]
            )
        )
    )

    page.add(
        ft.Row(
            spacing= 60,
            alignment= ft.MainAxisAlignment.CENTER,
            vertical_alignment= ft.CrossAxisAlignment.CENTER,
            controls=[
                maquina,
                billetes
            ]
        )
    )

ft.run(main , assets_dir= 'assets')
