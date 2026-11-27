"""Variantes de ``ft.DataTable``."""

from collections.abc import Sequence

import flet as ft


W = ft.FontWeight
Row = Sequence[str]


def _header(names: Sequence[str], numeric: set[int] = frozenset()) -> list[ft.DataColumn]:
    return [
        ft.DataColumn(ft.Text(name, weight=W.BOLD), numeric=i in numeric)
        for i, name in enumerate(names)
    ]


def _rows(rows: Sequence[Row], *, striped: bool = False, size: int | None = None) -> list[ft.DataRow]:
    return [
        ft.DataRow(
            cells=[ft.DataCell(ft.Text(value, size=size)) for value in row],
            color=ft.Colors.SURFACE_CONTAINER_LOW if striped and i % 2 else None,
        )
        for i, row in enumerate(rows)
    ]


def _badge(text: str, bg: ft.Colors, fg: ft.Colors) -> ft.Control:
    return ft.Container(
        padding=6, border_radius=20, bgcolor=bg, content=ft.Text(text, color=fg, size=11)
    )


def _status_row(order: str, customer: str, badge: ft.Control) -> ft.DataRow:
    return ft.DataRow(
        cells=[
            ft.DataCell(ft.Text(order)),
            ft.DataCell(ft.Text(customer)),
            ft.DataCell(badge),
            ft.DataCell(ft.IconButton(ft.Icons.MORE_VERT, tooltip="Más opciones")),
        ]
    )


def _basic() -> ft.DataTable:
    return ft.DataTable(
        columns=_header(["Nombre", "Área", "Estado"]),
        rows=_rows([
            ["Ana López", "Diseño", "Activo"],
            ["Luis Pérez", "Finanzas", "Activo"],
            ["Marta Ruiz", "Operaciones", "Pendiente"],
        ]),
    )


def _striped() -> ft.DataTable:
    return ft.DataTable(
        show_checkbox_column=False,
        heading_row_color=ft.Colors.INDIGO_300,
        column_spacing=24,
        columns=_header(["Fecha", "Concepto", "Categoría", "MXN"], numeric={3}),
        rows=_rows(
            [
                ["03 nov", "Supermercado", "Comida", "−$820"],
                ["02 nov", "Nómina", "Ingreso", "+$18,500"],
                ["01 nov", "Transporte", "Movilidad", "−$240"],
                ["31 oct", "Internet", "Servicios", "−$599"],
            ],
            striped=True,
        ),
    )


def _compact() -> ft.DataTable:
    return ft.DataTable(
        heading_row_height=38,
        data_row_min_height=34,
        data_row_max_height=40,
        column_spacing=18,
        columns=_header(["ID", "Archivo", "Tamaño"]),
        rows=_rows(
            [["01", "reporte.csv", "24 KB"], ["02", "ventas.xlsx", "1.2 MB"], ["03", "resumen.pdf", "840 KB"]],
            size=12,
        ),
    )


def _statuses() -> ft.DataTable:
    return ft.DataTable(
        columns=_header(["Pedido", "Cliente", "Estado", "Acción"]),
        rows=[
            _status_row("#2048", "Sofía Martínez", _badge("Enviado", ft.Colors.GREEN_100, ft.Colors.GREEN_900)),
            _status_row("#2049", "Diego Torres", _badge("En proceso", ft.Colors.AMBER_100, ft.Colors.AMBER_900)),
        ],
    )


def _comparison() -> ft.DataTable:
    check = lambda: ft.DataCell(ft.Icon(ft.Icons.CHECK))  # noqa: E731
    return ft.DataTable(
        columns=_header(["Plan", "Básico", "Pro", "Equipo"]),
        rows=[
            *_rows([["Proyectos", "3", "Ilimitados", "Ilimitados"], ["Colaboradores", "1", "5", "Ilimitados"]]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("Soporte")), check(), check(), check()]),
        ],
    )


@ft.component
def TableSection(title: str, description: str, table: ft.Control) -> ft.Control:
    return ft.Container(
        padding=18,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=16,
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text(title, size=18, weight=W.BOLD),
                ft.Text(description, size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                ft.Row([table], scroll=ft.ScrollMode.AUTO),
            ],
        ),
    )


@ft.component
def TablesGallery() -> ft.Control:
    return ft.Column(
        spacing=18,
        controls=[
            TableSection("Tabla básica", "Filas y columnas de texto.", _basic(), key="basic"),
            TableSection("Filas alternadas y números", "Movimientos con columna numérica alineada.", _striped(), key="striped"),
            TableSection("Tabla compacta", "Alturas reducidas para listados densos.", _compact(), key="compact"),
            TableSection("Celdas con estado y acciones", "Las celdas aceptan cualquier control, como etiquetas o iconos.", _statuses(), key="status"),
            TableSection("Comparación", "Columnas con indicadores para contrastar opciones.", _comparison(), key="compare"),
        ],
    )
