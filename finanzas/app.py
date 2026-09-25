from datetime import date
import os
from pathlib import Path
import sqlite3
import flet as ft
from .modelo import CATEGORIAS, Repositorio, moneda, resumir


def main(page: ft.Page):
    page.title = "Balance · Panel de gastos"
    page.padding = 24
    page.scroll = ft.ScrollMode.AUTO
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.TEAL)
    page.theme_mode = ft.ThemeMode.LIGHT
    ruta = Path(os.environ.get("FLET_DATA_DIR", str(Path.home() / ".fletBD"))) / "finanzas.sqlite3"
    try:
        repo = Repositorio(ruta)
    except (OSError, sqlite3.Error) as error:
        page.add(ft.Text(f"No se pudo abrir el almacenamiento: {error}"))
        return

    concepto = ft.TextField(label="Concepto", max_length=80)
    importe = ft.TextField(label="Importe (MXN)", hint_text="Ej. 120.50", helper="Sin separador de miles; máximo dos decimales")
    fecha = ft.TextField(label="Fecha (AAAA-MM-DD)", value=date.today().isoformat())
    categoria = ft.Dropdown(label="Categoría", value="Comida", options=[ft.DropdownOption(key=c, text=c) for c in CATEGORIAS])
    filtro = ft.Dropdown(label="Filtrar categoría", value="Todas", options=[ft.DropdownOption(key=c, text=c) for c in ("Todas", *CATEGORIAS)])
    mes = ft.TextField(label="Mes (AAAA-MM), vacío = todos", hint_text="2026-09")
    estado = ft.Text("Registra tu primer gasto. Todos los importes se expresan en MXN.")
    resumen = ft.ResponsiveRow()
    barras = ft.Column(spacing=14)
    alcance = ft.Text()
    tabla = ft.DataTable(columns=[ft.DataColumn(ft.Text(t)) for t in ("Fecha", "Concepto", "Categoría", "MXN", "Acción")])
    vacio = ft.Text("No hay gastos para estos filtros.")
    categoria_activa, mes_activo = "Todas", ""

    def tarjeta(titulo, valor):
        return ft.Container(col={"xs":12,"sm":6}, padding=20, border_radius=14,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            content=ft.Column([ft.Text(titulo), ft.Text(str(valor), size=30, weight=ft.FontWeight.BOLD)]))

    def mostrar(gastos):
        datos = resumir(gastos)
        alcance.value = f"Resultados: {categoria_activa} · {mes_activo or 'todos los meses'}"
        resumen.controls = [tarjeta("Total del filtro · MXN", moneda(datos["total"])), tarjeta("Movimientos del filtro", datos["cantidad"])]
        tabla.rows = [ft.DataRow(cells=[ft.DataCell(ft.Text(g.fecha)), ft.DataCell(ft.Text(g.concepto)),
            ft.DataCell(ft.Text(g.categoria)), ft.DataCell(ft.Text(moneda(g.centavos))),
            ft.DataCell(ft.IconButton(ft.Icons.DELETE_OUTLINE, tooltip="Eliminar gasto", on_click=lambda e, gasto=g: confirmar_borrado(gasto)))]) for g in gastos]
        vacio.visible = not bool(gastos)
        tabla.visible = bool(gastos)
        barras.controls = [ft.Column([ft.Text(f"{cat} · {moneda(valor)} · {valor/datos['total']:.1%}"),
            ft.ProgressBar(value=valor/datos["total"])]) for cat, valor in sorted(datos["categorias"].items(), key=lambda x:x[1], reverse=True)]
        if not gastos:
            barras.controls = [ft.Text("Las proporciones aparecerán al registrar gastos.")]
        page.update()

    def actualizar():
        mostrar(repo.listar(categoria_activa, mes_activo))

    def aplicar(e=None):
        nonlocal categoria_activa, mes_activo
        try:
            mes_nuevo = (mes.value or "").strip()
            gastos = repo.listar(filtro.value, mes_nuevo)
            categoria_activa, mes_activo = filtro.value, mes_nuevo
            mes.error_text = None
            estado.value = "Filtros aplicados"
            mostrar(gastos)
        except (ValueError, sqlite3.Error) as error:
            mes.error_text = str(error)
            estado.value = "Filtro no aplicado; se conservan los resultados anteriores."
            page.update()

    def guardar(e):
        try:
            repo.agregar(fecha.value or "", concepto.value or "", categoria.value, importe.value or "")
            concepto.value = ""
            importe.value = ""
            estado.value = "Gasto guardado. Si no aparece, revisa los filtros activos."
            actualizar()
        except (ValueError, sqlite3.Error) as error:
            estado.value = f"No se guardó: {error}"
            page.update()

    def confirmar_borrado(gasto):
        def borrar(e):
            page.pop_dialog()
            try:
                repo.eliminar(gasto.id)
                estado.value = "Gasto eliminado"
                actualizar()
            except (ValueError, sqlite3.Error) as error:
                estado.value = f"No se eliminó: {error}"
                page.update()
        page.show_dialog(ft.AlertDialog(modal=True, title=ft.Text("¿Eliminar este gasto?"),
            content=ft.Text(f"{gasto.concepto} · {moneda(gasto.centavos)}"),
            actions=[ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()), ft.TextButton("Eliminar", on_click=borrar)]))

    for control in (concepto, importe, fecha, categoria):
        control.col = {"xs":12,"md":6}
    page.add(ft.Row([ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=32), ft.Text("Balance", size=36, weight=ft.FontWeight.BOLD)], wrap=True),
        ft.Text("Comprende tus gastos · demostración local · MXN"),
        ft.Card(content=ft.Container(padding=20, content=ft.Column([ft.Text("Nuevo movimiento", size=22),
            ft.ResponsiveRow([concepto, importe, fecha, categoria]), ft.Button("Registrar gasto", icon=ft.Icons.ADD, on_click=guardar)]))),
        estado, ft.Divider(), filtro, mes, ft.Button("Aplicar filtros", on_click=aplicar), alcance, resumen,
        ft.Text("Distribución del total filtrado", size=24), barras,
        ft.Text("Movimientos", size=24), vacio, ft.Row([tabla], scroll=ft.ScrollMode.AUTO),
        ft.Text("Datos locales de un usuario. No se conecta a cuentas bancarias.", size=12))
    try:
        actualizar()
    except sqlite3.Error as error:
        estado.value = f"No se pudieron cargar los datos: {error}"
        page.update()


if __name__ == "__main__":
    ft.run(main)
