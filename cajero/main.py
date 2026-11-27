from collections.abc import Awaitable, Callable

import flet as ft
import flet_audio as fta

try:
    from .model import Cajero
except ImportError:  # Permite ejecutar: python main.py desde esta carpeta.
    from model import Cajero

MAX_DIGITOS = 5
COLOR_ERROR = ft.Colors.PINK_ACCENT_700
COLOR_EXITO = ft.Colors.with_opacity(0.8, ft.Colors.CYAN_ACCENT)

Handler = Callable[[ft.Event[ft.Button]], Awaitable[None] | None]


def billete_card(denominacion: int) -> ft.Card:
    """Tarjeta que representa un billete entregado."""
    return ft.Card(
        elevation=10,
        shadow_color=ft.Colors.LIME,
        content=ft.Container(
            width=120,
            height=50,
            alignment=ft.Alignment.CENTER,
            border_radius=8,
            bgcolor=ft.Colors.GREEN_900,
            shadow=ft.BoxShadow(
                blur_radius=12,
                color=ft.Colors.with_opacity(0.2, ft.Colors.GREEN_ACCENT_400),
            ),
            content=ft.Container(
                width=104,
                height=40,
                padding=ft.Padding.symmetric(horizontal=20),
                alignment=ft.Alignment.CENTER,
                border_radius=6,
                bgcolor=ft.Colors.GREEN_ACCENT_400,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Icon(
                            ft.Icons.MONETIZATION_ON_OUTLINED,
                            size=18,
                            color=ft.Colors.AMBER_ACCENT_700,
                        ),
                        ft.Text(
                            str(denominacion),
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREEN_900,
                        ),
                    ],
                ),
            ),
        ),
    )


def boton(texto: str, on_click: Handler) -> ft.Button:
    """Tecla del teclado del cajero."""
    return ft.Button(
        content=texto,
        width=74,
        height=36,
        on_click=on_click,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREY_700,
            color=ft.Colors.WHITE,
            overlay_color=ft.Colors.CYAN_700,
            shape=ft.RoundedRectangleBorder(radius=6),
            padding=0,
            text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
        ),
    )


class CajeroView:
    """Estado y controles de la pantalla del cajero."""

    def __init__(self, page: ft.Page, cajero: Cajero | None = None) -> None:
        self.page = page
        self.cajero = cajero or Cajero()

        self.click = fta.Audio(
            src="/audio/click.wav", volume=0.2, release_mode=fta.ReleaseMode.STOP
        )
        self.success = fta.Audio(
            src="/audio/success.wav", volume=0.4, release_mode=fta.ReleaseMode.STOP
        )

        page.services.extend([self.click, self.success])

        self.monto = ft.Text(
            size=20,
            weight=ft.FontWeight.W_800,
            color=ft.Colors.BLACK,
            text_align=ft.TextAlign.END,
        )
        self.status = ft.Text()
        self.billetes = ft.Column(
            spacing=0,
            height=470,
            wrap=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # Events
    async def on_digito(self, e: ft.Event[ft.Button]) -> None:
        digito = e.control.content
        if len(self.monto.value or "") < MAX_DIGITOS:
            self.monto.value = (self.monto.value or "") + digito
            await self.click.play()

    def on_borrar(self, e: ft.Event[ft.Button]) -> None:
        self.monto.value = (self.monto.value or "")[:-1]

    async def on_enter(self, e: ft.Event[ft.Button]) -> None:
        if self.retirar():
            self.monto.value = ""
            await self.success.play()

    # Lógica de representatación
    def retirar(self) -> bool:
        """Procesa el monto capturado y actualiza estado y billetes."""
        texto = (self.monto.value or "").strip()
        if not texto:
            return self._rechazar("Ingresa un monto para retirar")

        mensaje, autorizado = self.cajero.mensaje_retiro(int(texto))
        if not autorizado:
            return self._rechazar(mensaje)

        self.billetes.controls = [
            billete_card(b) for b in self.cajero.entregar_dinero(int(texto))
        ]
        self.status.value = mensaje
        self.status.color = COLOR_EXITO
        return True

    def _rechazar(self, mensaje: str) -> bool:
        self.billetes.controls = []
        self.status.value = mensaje
        self.status.color = COLOR_ERROR
        return False

    # Construncción de UI
    def teclado(self) -> ft.Column:
        filas: list[ft.Control] = [
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[boton(str(n), self.on_digito) for n in range(inicio, inicio + 3)],
            )
            for inicio in (1, 4, 7)
        ]
        filas.append(
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    boton("0", self.on_digito),
                    boton("BORRAR", self.on_borrar),
                    boton("ENTER", self.on_enter),
                ],
            )
        )
        return ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=filas,
        )

    def build(self) -> ft.Row:
        display = ft.Container(
            width=240,
            height=56,
            padding=10,
            bgcolor=ft.Colors.WHITE,
            border_radius=8,
            alignment=ft.Alignment.CENTER_RIGHT,
            shadow=ft.BoxShadow(
                blur_radius=20,
                color=ft.Colors.with_opacity(0.4, ft.Colors.CYAN_ACCENT),
            ),
            content=self.monto,
        )
        maquina = ft.Card(
            content=ft.Container(
                width=300,
                height=440,
                padding=20,
                border_radius=10,
                alignment=ft.Alignment.TOP_CENTER,
                bgcolor=ft.Colors.GREY_900,
                border=ft.Border.all(1, "#3D4251"),
                shadow=ft.BoxShadow(
                    blur_radius=20, color=ft.Colors.with_opacity(0.8, "#00E8C6")
                ),
                content=ft.Column(
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            "BBVA",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.CYAN_500,
                        ),
                        display,
                        self.status,
                        self.teclado(),
                    ],
                ),
            )
        )
        return ft.Row(
            spacing=60,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[maquina, self.billetes],
        )


def main(page: ft.Page) -> None:
    page.title = "ATM with FLET"
    page.window.width = 720
    page.window.alignment = ft.Alignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 40

    page.add(CajeroView(page).build())


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
