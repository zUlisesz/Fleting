"""Suma de números binarios con Flet 1.0: UI declarativa (componentes + hooks).

    python3 main.py        # desde esta carpeta, o: flet run
"""

import flet as ft

from binario import MAX_BITS, Suma, es_binario, sumar

APP_TITLE = "Binary Addition"
ACCENT = ft.Colors.INDIGO_500
MAX_CELL = 38  # lado máximo de una casilla de bit
MIN_CELL = 16
GAP = 4  # separación entre casillas
SHEET_WIDTH = 480  # ancho disponible para la suma dentro de la tarjeta
OPERATOR_COLUMN = 28  # ancho de la columna del signo «+»


def strip_zeros(bits: str) -> str:
    """Quita ceros a la izquierda sin vaciar el valor (``"0010"`` → ``"10"``)."""
    return bits.lstrip("0") or "0"


def cell_size(columns: int) -> int:
    """Lado de casilla para que ``columns`` columnas quepan en la tarjeta."""
    return max(MIN_CELL, min(MAX_CELL, (SHEET_WIDTH - OPERATOR_COLUMN) // columns - GAP))


@ft.component
def Bit(value: str, *, size: int, filled: bool = False) -> ft.Control:
    """Un bit: lleno si es ``1`` y atenuado si es ``0``."""
    on = filled and value == "1"
    return ft.Container(
        width=size,
        height=size,
        border_radius=size * 0.3,
        alignment=ft.Alignment.CENTER,
        bgcolor=ACCENT if on else ft.Colors.with_opacity(0.08, ft.Colors.ON_SURFACE),
        content=ft.Text(
            value,
            size=size * 0.5,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE if on else ft.Colors.ON_SURFACE_VARIANT,
        ),
    )


@ft.component
def BitRow(bits: str, *, size: int, skip: int = 0, filled: bool = False, operator: str = "") -> ft.Control:
    """Fila de casillas alineada a la derecha; ``skip`` casillas vacías al inicio."""
    return ft.Row(
        spacing=GAP,
        alignment=ft.MainAxisAlignment.END,
        controls=[
            ft.Container(
                width=OPERATOR_COLUMN,
                content=ft.Text(operator, size=22, weight=ft.FontWeight.BOLD, color=ACCENT),
            ),
            *[ft.Container(width=size, height=size) for _ in range(skip)],
            *[Bit(bit, size=size, filled=filled) for bit in bits],
        ],
    )


@ft.component
def CarryRow(carries: str, *, size: int) -> ft.Control:
    """Acarreo que entra a cada columna: solo se dibujan los que valen 1."""
    small = size * 3 // 5
    return ft.Row(
        spacing=GAP,
        alignment=ft.MainAxisAlignment.END,
        controls=[
            ft.Container(width=OPERATOR_COLUMN),
            *[
                ft.Container(
                    width=size,
                    height=small,
                    alignment=ft.Alignment.CENTER,
                    content=Bit("1", size=small, filled=True) if carry == "1" else None,
                )
                for carry in carries
            ],
        ],
    )


@ft.component
def AdditionSheet(suma: Suma) -> ft.Control:
    """La suma escrita "en papel": acarreos, sumandos, línea y resultado."""
    size = cell_size(suma.ancho)
    result = strip_zeros(suma.resultado)
    return ft.Column(
        spacing=6,
        horizontal_alignment=ft.CrossAxisAlignment.END,
        controls=[
            ft.Text("Acarreos", size=11, color=ft.Colors.ON_SURFACE_VARIANT),
            CarryRow(suma.acarreos, size=size),
            BitRow(suma.primero, size=size, skip=suma.ancho - len(suma.primero)),
            BitRow(suma.segundo, size=size, skip=suma.ancho - len(suma.segundo), operator="+"),
            ft.Divider(height=8, thickness=2, color=ACCENT),
            BitRow(result, size=size, skip=suma.ancho - len(result), filled=True),
        ],
    )


@ft.component
def Equivalence(suma: Suma) -> ft.Control:
    """``5 + 3 = 8``: la misma operación en decimal."""
    a, b, total = suma.decimal
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=16, vertical=10),
        border_radius=12,
        bgcolor=ft.Colors.with_opacity(0.08, ACCENT),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.TAG, size=18, color=ACCENT),
                ft.Text(f"{a} + {b} = {total}", size=16, weight=ft.FontWeight.W_600),
                ft.Text("en decimal", size=12, color=ft.Colors.ON_SURFACE_VARIANT),
            ],
        ),
    )


@ft.component
def BinaryField(label: str, value: str, *, on_change, autofocus: bool = False) -> ft.Control:
    """Campo que solo acepta ``0`` y ``1``."""
    return ft.TextField(
        label=label,
        value=value,
        autofocus=autofocus,
        max_length=MAX_BITS,
        counter=ft.Text(""),  # oculta el contador de caracteres
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.InputFilter(regex_string=r"[01]", allow=True),
        border_radius=14,
        text_size=18,
        prefix_icon=ft.Icons.LOOKS_ONE_OUTLINED,
        on_change=lambda e: on_change(e.control.value),
    )


@ft.component
def Placeholder(message: str) -> ft.Control:
    return ft.Container(
        height=160,
        alignment=ft.Alignment.CENTER,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.CALCULATE_OUTLINED, size=40, color=ft.Colors.OUTLINE),
                ft.Text(message, color=ft.Colors.ON_SURFACE_VARIANT, text_align=ft.TextAlign.CENTER),
            ],
        ),
    )


@ft.component
def App() -> ft.Control:
    first, set_first = ft.use_state("")
    second, set_second = ft.use_state("")

    ready = es_binario(first) and es_binario(second)
    suma = ft.use_memo(lambda: sumar(first, second) if ready else None, [first, second])

    def clear() -> None:
        set_first("")
        set_second("")

    result: ft.Control = (
        ft.Column(
            spacing=16,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[AdditionSheet(suma), Equivalence(suma)],
        )
        if suma
        else Placeholder("Escribe dos números binarios y el resultado aparece aquí.")
    )

    return ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=[ft.Colors.INDIGO_50, ft.Colors.PURPLE_50, ft.Colors.CYAN_50],
        ),
        content=ft.Card(
            elevation=8,
            shape=ft.RoundedRectangleBorder(radius=24),
            content=ft.Container(
                width=560,
                padding=36,
                content=ft.Column(
                    tight=True,
                    spacing=20,
                    controls=[
                        ft.Row(
                            spacing=14,
                            controls=[
                                ft.Container(
                                    padding=12,
                                    border_radius=14,
                                    bgcolor=ACCENT,
                                    content=ft.Icon(ft.Icons.ADD_ROUNDED, color=ft.Colors.WHITE),
                                ),
                                ft.Column(
                                    spacing=0,
                                    controls=[
                                        ft.Text(APP_TITLE, size=24, weight=ft.FontWeight.BOLD),
                                        ft.Text(
                                            "Suma dos números en base 2",
                                            size=13,
                                            color=ft.Colors.ON_SURFACE_VARIANT,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        BinaryField("Primer número", first, on_change=set_first, autofocus=True),
                        BinaryField("Segundo número", second, on_change=set_second),
                        ft.Divider(height=1),
                        result,
                        ft.OutlinedButton(
                            "Limpiar",
                            icon=ft.Icons.CLEANING_SERVICES_OUTLINED,
                            disabled=not (first or second),
                            on_click=lambda _: clear(),
                        ),
                    ],
                ),
            ),
        ),
    )


def main(page: ft.Page) -> None:
    page.title = APP_TITLE
    page.padding = 0
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 720
    page.window.height = 820
    page.render(App)


if __name__ == "__main__":
    ft.run(main)
