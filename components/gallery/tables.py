"""Galería de tablas Flet con estilos y contenido de distintas clases."""

import flet as ft


def _section(title: str, description: str, table: ft.Control) -> ft.Container:
    return ft.Container(
        padding=18,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=16,
        content=ft.Column([ft.Text(title, size=18, weight=ft.FontWeight.BOLD), ft.Text(description, size=12, color=ft.Colors.ON_SURFACE_VARIANT), ft.Row([table], scroll=ft.ScrollMode.AUTO)], spacing=12),
    )


def _data_table(columns: list[str], rows: list[list[str]], *, numeric: set[int] | None = None, heading: str | None = None, color: str | None = None) -> ft.DataTable:
    return ft.DataTable(
        show_checkbox_column=False,
        heading_row_color=color or ft.Colors.SURFACE_CONTAINER_HIGHEST,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=10,
        column_spacing=24,
        columns=[ft.DataColumn(ft.Text(name, weight=ft.FontWeight.BOLD), numeric=bool(numeric and i in numeric)) for i, name in enumerate(columns)],
        rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(value, weight=ft.FontWeight.W_600 if heading and r == 0 else None)) for value in row], color=ft.Colors.SURFACE_CONTAINER_LOW if r % 2 else None) for r, row in enumerate(rows)],
    )


def table_gallery() -> ft.Column:
    """Muestra tablas con variantes para datos tabulares y comparativos."""
    basic = _data_table(["Nombre", "Área", "Estado"], [["Ana López", "Diseño", "Activo"], ["Luis Pérez", "Finanzas", "Activo"], ["Marta Ruiz", "Operaciones", "Pendiente"]])
    striped = _data_table(["Fecha", "Concepto", "Categoría", "MXN"], [["03 nov", "Supermercado", "Comida", "−$820"], ["02 nov", "Nómina", "Ingreso", "+$18,500"], ["01 nov", "Transporte", "Movilidad", "−$240"], ["31 oct", "Internet", "Servicios", "−$599"]], numeric={3}, color=ft.Colors.INDIGO_50)
    compact = ft.DataTable(heading_row_height=38, data_row_min_height=34, data_row_max_height=40, column_spacing=18, columns=[ft.DataColumn(ft.Text(x)) for x in ["ID", "Archivo", "Tamaño"]], rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(x, size=12)) for x in row]) for row in [["01", "reporte.csv", "24 KB"], ["02", "ventas.xlsx", "1.2 MB"], ["03", "resumen.pdf", "840 KB"]]])
    statuses = ft.DataTable(columns=[ft.DataColumn(ft.Text(x)) for x in ["Pedido", "Cliente", "Estado", "Acción"]], rows=[ft.DataRow(cells=[ft.DataCell(ft.Text("#2048")), ft.DataCell(ft.Text("Sofía Martínez")), ft.DataCell(ft.Container(padding=6, border_radius=20, bgcolor=ft.Colors.GREEN_100, content=ft.Text("Enviado", color=ft.Colors.GREEN_900, size=11))), ft.DataCell(ft.IconButton(ft.Icons.MORE_VERT, tooltip="Más opciones"))]), ft.DataRow(cells=[ft.DataCell(ft.Text("#2049")), ft.DataCell(ft.Text("Diego Torres")), ft.DataCell(ft.Container(padding=6, border_radius=20, bgcolor=ft.Colors.AMBER_100, content=ft.Text("En proceso", color=ft.Colors.AMBER_900, size=11))), ft.DataCell(ft.IconButton(ft.Icons.MORE_VERT, tooltip="Más opciones"))])])
    comparison = ft.DataTable(columns=[ft.DataColumn(ft.Text("Plan")), ft.DataColumn(ft.Text("Básico")), ft.DataColumn(ft.Text("Pro")), ft.DataColumn(ft.Text("Equipo"))], rows=[ft.DataRow(cells=[ft.DataCell(ft.Text("Proyectos")), ft.DataCell(ft.Text("3")), ft.DataCell(ft.Text("Ilimitados")), ft.DataCell(ft.Text("Ilimitados"))]), ft.DataRow(cells=[ft.DataCell(ft.Text("Colaboradores")), ft.DataCell(ft.Text("1")), ft.DataCell(ft.Text("5")), ft.DataCell(ft.Text("Ilimitados"))]), ft.DataRow(cells=[ft.DataCell(ft.Text("Soporte")), ft.DataCell(ft.Icon(ft.Icons.CHECK)), ft.DataCell(ft.Icon(ft.Icons.CHECK)), ft.DataCell(ft.Icon(ft.Icons.CHECK))])])
    return ft.Column([ft.Text("Tables", size=24, weight=ft.FontWeight.BOLD), ft.Text("Variantes de ft.DataTable para listados, estados, métricas y comparación."), _section("Tabla básica", "Filas y columnas de texto.", basic), _section("Filas alternadas y números", "Registros tipo movimientos financieros con columna numérica alineada.", striped), _section("Tabla compacta", "Alturas reducidas para listados densos.", compact), _section("Celdas con estado y acciones", "Las celdas aceptan controles Flet, como etiquetas e iconos interactivos.", statuses), _section("Comparación", "Columnas con indicadores para contrastar opciones.", comparison)], spacing=18)


def main(page: ft.Page) -> None:
    page.title = "Flet Tables"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    page.add(table_gallery())


if __name__ == "__main__":
    ft.run(main)
