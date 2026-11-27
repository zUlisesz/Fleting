"""Componentes declarativos de la interfaz de finanzas."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from datetime import date

import flet as ft

from .dominio import (
    CATEGORIAS,
    CATEGORIAS_FILTRO,
    TIPOS,
    TIPOS_FILTRO,
    Filtros,
    Movimiento,
    Resumen,
    moneda,
    moneda_firmada,
)

VERDE = ft.Colors.GREEN_700
ROJO = ft.Colors.RED_700
COLUMNAS_TARJETA = {"xs": 12, "sm": 6, "md": 3}
COLUMNAS_CAMPO = {"xs": 12, "md": 6}


def opciones(valores: Sequence[str]) -> list[ft.DropdownOption]:
    return [ft.DropdownOption(key=v, text=v) for v in valores]


@ft.component
def Rejilla(hijos: Sequence[ft.Control], *, columnas: dict[str, int]) -> ft.Control:
    """``ResponsiveRow`` cuyos hijos ocupan ``columnas``.
    ``col`` se aplica a un contenedor propio: ``ResponsiveRow`` lo lee de sus
    hijos directos y un componente no lo expone.
    """
    return ft.ResponsiveRow(
        spacing=16,
        run_spacing=16,
        controls=[ ft.Container(col=columnas, content=h) for h in hijos],
    )


# Encabezado y perfiles 

@ft.component
def Encabezado(*, oscuro: bool, on_tema: Callable[[bool], None]) -> ft.Control:
    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Row(
                controls=[
                    ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=32),
                    ft.Text("Balance", size=36, weight=ft.FontWeight.BOLD),
                ]
            ),
            ft.Switch(
                value=oscuro,
                thumb_icon=ft.Icons.SUNNY,
                tooltip="Tema oscuro",
                on_change=lambda e: on_tema(bool(e.control.value)),
            ),
        ],
    )


@ft.component
def SelectorPerfil(
    perfiles: Sequence[tuple[int, str]],
    perfil_id: int,
    *,
    on_seleccionar: Callable[[int], None],
    on_crear: Callable[[str], bool],
) -> ft.Control:
    """Dropdown de perfiles y alta de uno nuevo (``on_crear`` devuelve si tuvo éxito)."""
    nombre, set_nombre = ft.use_state("")

    def crear(_) -> None:
        if on_crear(nombre):
            set_nombre("")

    return ft.Row(
        wrap=True,
        controls=[
            ft.Dropdown(
                label="Perfil",
                value=str(perfil_id),
                options=[ft.DropdownOption(key=str(i), text=n) for i, n in perfiles],
                on_select=lambda e: on_seleccionar(int(e.control.value)),
            ),
            ft.TextField(
                label="Nombre del nuevo perfil",
                value=nombre,
                max_length=80,
                on_change=lambda e: set_nombre(e.control.value),
            ),
            ft.Button("Crear perfil", on_click=crear),
        ],
    )


# Formulario y filtros

@ft.component
def FormularioMovimiento(*, on_guardar: Callable[..., bool]) -> ft.Control:
    """Campos de un movimiento nuevo.

    ``on_guardar(fecha, concepto, categoria, tipo, importe)`` devuelve ``True``
    si se guardó; entonces se limpian concepto e importe.
    """
    concepto, set_concepto = ft.use_state("")
    importe, set_importe = ft.use_state("")
    fecha, set_fecha = ft.use_state(lambda: date.today().isoformat())
    categoria, set_categoria = ft.use_state("Comida")
    tipo, set_tipo = ft.use_state("Gasto")

    def guardar(_) -> None:
        if on_guardar(fecha, concepto, categoria, tipo, importe):
            set_concepto("")
            set_importe("")

    return ft.Card(
        content=ft.Container(
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text("Nuevo movimiento", size=22),
                    ft.ResponsiveRow(
                        controls=[
                            ft.TextField(
                                label="Concepto", value=concepto, max_length=80, col=COLUMNAS_CAMPO,
                                on_change=lambda e: set_concepto(e.control.value),
                            ),
                            ft.TextField(
                                label="Importe (MXN)", value=importe, hint_text="Ej. 120.50",
                                helper="Sin separador de miles; máximo dos decimales",
                                col=COLUMNAS_CAMPO,
                                on_change=lambda e: set_importe(e.control.value),
                            ),
                            ft.TextField(
                                label="Fecha (AAAA-MM-DD)", value=fecha, col=COLUMNAS_CAMPO,
                                on_change=lambda e: set_fecha(e.control.value),
                            ),
                            ft.Dropdown(
                                label="Categoría", value=categoria, options=opciones(CATEGORIAS),
                                col=COLUMNAS_CAMPO, on_select=lambda e: set_categoria(e.control.value),
                            ),
                            ft.Dropdown(
                                label="Tipo", value=tipo, options=opciones(TIPOS),
                                col=COLUMNAS_CAMPO, on_select=lambda e: set_tipo(e.control.value),
                            ),
                        ]
                    ),
                    ft.Button("Registrar movimiento", icon=ft.Icons.ADD, on_click=guardar),
                ]
            ),
        )
    )


@ft.component
def PanelFiltros(
    aplicados: Filtros, *, on_aplicar: Callable[[Filtros], str | None]
) -> ft.Control:
    """Borrador de filtros. ``on_aplicar`` devuelve un error o ``None`` si se aplicó."""
    categoria, set_categoria = ft.use_state(aplicados.categoria)
    tipo, set_tipo = ft.use_state(aplicados.tipo)
    mes, set_mes = ft.use_state(aplicados.mes)
    error, set_error = ft.use_state(None)

    def aplicar(_) -> None:
        set_error(on_aplicar(Filtros(categoria, mes.strip(), tipo)))

    return ft.Column(
        controls=[
            ft.ResponsiveRow(
                controls=[
                    ft.Dropdown(
                        label="Filtrar categoría", value=categoria, options=opciones(CATEGORIAS_FILTRO),
                        col={"xs": 12, "md": 4}, on_select=lambda e: set_categoria(e.control.value),
                    ),
                    ft.Dropdown(
                        label="Filtrar tipo", value=tipo, options=opciones(TIPOS_FILTRO),
                        col={"xs": 12, "md": 4}, on_select=lambda e: set_tipo(e.control.value),
                    ),
                    ft.TextField(
                        label="Mes (AAAA-MM), vacío = todos", hint_text="2026-09", value=mes,
                        error=error, col={"xs": 12, "md": 4},
                        on_change=lambda e: set_mes(e.control.value),
                    ),
                ]
            ),
            ft.Button("Aplicar filtros", on_click=aplicar),
        ]
    )


# Resultados

@ft.component
def TarjetaResumen(titulo: str, valor: str, color: str | None = None) -> ft.Control:
    return ft.Container(
        padding=20,
        border_radius=14,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        content=ft.Column(
            controls=[ft.Text(titulo), ft.Text(valor, size=28, weight=ft.FontWeight.BOLD, color=color)]
        ),
    )


@ft.component
def PanelResumen(resumen: Resumen) -> ft.Control:
    return Rejilla(
        [
            TarjetaResumen("Ingresos · MXN", moneda(resumen.ingresos), VERDE, key="ingresos"),
            TarjetaResumen("Gastos · MXN", moneda(resumen.gastos), ROJO, key="gastos"),
            TarjetaResumen(
                "Saldo del filtro · MXN",
                moneda_firmada(resumen.balance),
                VERDE if resumen.balance >= 0 else ROJO,
                key="saldo",
            ),
            TarjetaResumen("Movimientos", str(resumen.cantidad), key="cantidad"),
        ],
        columnas=COLUMNAS_TARJETA,
    )


@ft.component
def Distribucion(resumen: Resumen) -> ft.Control:
    """Barras con la proporción de cada «tipo · categoría» sobre el total filtrado."""
    if not resumen.total:
        return ft.Text("Las proporciones aparecerán al registrar movimientos.")
    ordenadas = sorted(resumen.categorias.items(), key=lambda par: par[1], reverse=True)
    return ft.Column(
        spacing=14,
        controls=[
            ft.Column(
                controls=[
                    ft.Text(f"{nombre} · {moneda(valor)} · {valor / resumen.total:.1%}"),
                    ft.ProgressBar(value=valor / resumen.total),
                ]
            )
            for nombre, valor in ordenadas
        ],
    )


@ft.component
def TablaMovimientos(
    movimientos: Sequence[Movimiento], *, on_eliminar: Callable[[Movimiento], None]
) -> ft.Control:
    if not movimientos:
        return ft.Text("No hay movimientos para estos filtros.")

    def fila(m: Movimiento) -> ft.DataRow:
        signo, color = ("+", VERDE) if m.es_ingreso else ("-", ROJO)
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(m.fecha)),
                ft.DataCell(ft.Text(m.concepto)),
                ft.DataCell(ft.Text(m.categoria)),
                ft.DataCell(ft.Text(m.tipo)),
                ft.DataCell(ft.Text(f"{signo}{moneda(m.centavos)}", color=color)),
                ft.DataCell(
                    ft.IconButton(
                        ft.Icons.DELETE_OUTLINE,
                        tooltip="Eliminar movimiento",
                        on_click=lambda _, m=m: on_eliminar(m),
                    )
                ),
            ]
        )

    return ft.Row(
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text(t))
                    for t in ("Fecha", "Concepto", "Categoría", "Tipo", "MXN", "Acción")
                ],
                rows=[fila(m) for m in movimientos],
            )
        ],
    )


@ft.component
def ConfirmarBorrado(
    movimiento: Movimiento, *, on_confirmar: Callable[[], None], on_cancelar: Callable[[], None]
) -> ft.Control:
    """Diálogo modal visible mientras el componente esté montado."""
    ft.use_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text("¿Eliminar este movimiento?"),
            content=ft.Text(f"{movimiento.concepto} · {moneda(movimiento.centavos)}"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: on_cancelar()),
                ft.TextButton("Eliminar", on_click=lambda _: on_confirmar()),
            ],
        )
    )
    return ft.Container(visible=False)
