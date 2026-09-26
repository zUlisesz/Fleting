from datetime import date
import os
from pathlib import Path
import sqlite3
import flet as ft
from .modelo import CATEGORIAS, TIPOS, TIPOS_FILTRO, Repositorio, moneda, moneda_firmada, resumir


def main(page: ft.Page):
    page.title = "Balance · Flujo de efectivo"
    page.padding = 24
    page.scroll = ft.ScrollMode.AUTO
    page.window.width = 880
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.TEAL)
    page.theme_mode = ft.ThemeMode.LIGHT
    ruta = Path(os.environ.get("FLET_DATA_DIR", str(Path.home() / ".fletBD"))) / "finanzas.sqlite3"
    try:
        repo = Repositorio(ruta)
    except (OSError, sqlite3.Error) as error:
        page.add(ft.Text(f"No se pudo abrir el almacenamiento: {error}"))
        return

    concepto = ft.TextField(label="Concepto", max_length=80)
    importe = ft.TextField(
        label="Importe (MXN)",
        hint_text="Ej. 120.50",
        helper="Sin separador de miles; máximo dos decimales",
    )
    fecha = ft.TextField(label="Fecha (AAAA-MM-DD)", value=date.today().isoformat())
    categoria = ft.Dropdown(
        label="Categoría",
        value="Comida",
        options=[ft.DropdownOption(key=c, text=c) for c in CATEGORIAS],
    )
    tipo = ft.Dropdown(
        label="Tipo",
        value="Gasto",
        options=[ft.DropdownOption(key=c, text=c) for c in TIPOS],
    )
    filtro = ft.Dropdown(
        label="Filtrar categoría",
        value="Todas",
        options=[ft.DropdownOption(key=c, text=c) for c in ("Todas", *CATEGORIAS)],
    )
    filtro_tipo = ft.Dropdown(
        label="Filtrar tipo",
        value="Todos",
        options=[ft.DropdownOption(key=t, text=t) for t in TIPOS_FILTRO],
    )
    mes = ft.TextField(label="Mes (AAAA-MM), vacío = todos", hint_text="2026-09")
    estado = ft.Text("Registra tu primer movimiento. Todos los importes se expresan en MXN.")
    resumen = ft.ResponsiveRow()
    barras = ft.Column(spacing=14)
    alcance = ft.Text()
    tabla = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(t)) for t in ("Fecha", "Concepto", "Categoría", "Tipo", "MXN", "Acción")]
    )
    vacio = ft.Text("No hay movimientos para estos filtros.")
    categoria_activa, mes_activo, tipo_activo = "Todas", "", "Todos"

    def tarjeta(titulo, valor, color=None):
        return ft.Container(
            col={"xs": 12, "sm": 6, "md": 3},
            padding=20,
            border_radius=14,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            content=ft.Column(
                [ft.Text(titulo), ft.Text(str(valor), size=28, weight=ft.FontWeight.BOLD, color=color)]
            ),
        )

    def mostrar(movimientos):
        datos = resumir(movimientos)
        alcance.value = f"Resultados: {categoria_activa} · {tipo_activo} · {mes_activo or 'todos los meses'}"
        saldo_color = ft.Colors.GREEN_700 if datos["balance"] >= 0 else ft.Colors.RED_700
        resumen.controls = [
            tarjeta("Ingresos · MXN", moneda(datos["ingresos"]), ft.Colors.GREEN_700),
            tarjeta("Gastos · MXN", moneda(datos["gastos"]), ft.Colors.RED_700),
            tarjeta("Saldo del filtro · MXN", moneda_firmada(datos["balance"]), saldo_color),
            tarjeta("Movimientos", datos["cantidad"]),
        ]
        tabla.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(movimiento.fecha)),
                    ft.DataCell(ft.Text(movimiento.concepto)),
                    ft.DataCell(ft.Text(movimiento.categoria)),
                    ft.DataCell(ft.Text(movimiento.tipo)),
                    ft.DataCell(
                        ft.Text(
                            f"{'+' if movimiento.tipo == 'Ingreso' else '-'}{moneda(movimiento.centavos)}",
                            color=ft.Colors.GREEN_700
                            if movimiento.tipo == "Ingreso"
                            else ft.Colors.RED_700,
                        )
                    ),
                    ft.DataCell(
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            tooltip="Eliminar movimiento",
                            on_click=lambda e, movimiento=movimiento: confirmar_borrado(movimiento),
                        )
                    ),
                ]
            )
            for movimiento in movimientos
        ]
        vacio.visible = not bool(movimientos)
        tabla.visible = bool(movimientos)
        if datos["total"]:
            barras.controls = [
                ft.Column(
                    [
                        ft.Text(f"{cat} · {moneda(valor)} · {valor / datos['total']:.1%}"),
                        ft.ProgressBar(value=valor / datos["total"]),
                    ]
                )
                for cat, valor in sorted(datos["categorias"].items(), key=lambda item: item[1], reverse=True)
            ]
        else:
            barras.controls = [ft.Text("Las proporciones aparecerán al registrar movimientos.")]
        page.update()

    def actualizar():
        mostrar(repo.listar(categoria_activa, mes_activo, tipo_activo))

    def aplicar(e=None):
        nonlocal categoria_activa, mes_activo, tipo_activo
        try:
            mes_nuevo = (mes.value or "").strip()
            movimientos = repo.listar(filtro.value, mes_nuevo, filtro_tipo.value)
            categoria_activa, mes_activo, tipo_activo = filtro.value, mes_nuevo, filtro_tipo.value
            mes.error_text = None
            estado.value = "Filtros aplicados"
            mostrar(movimientos)
        except (ValueError, sqlite3.Error) as error:
            mes.error_text = str(error)
            estado.value = "Filtro no aplicado; se conservan los resultados anteriores."
            page.update()

    def guardar(e):
        try:
            repo.agregar(
                fecha.value or "", concepto.value or "", categoria.value, tipo.value, importe.value or ""
            )
            concepto.value = ""
            importe.value = ""
            estado.value = "Movimiento guardado. Si no aparece, revisa los filtros activos."
            actualizar()
        except (ValueError, sqlite3.Error) as error:
            estado.value = f"No se guardó: {error}"
            page.update()

    def cambiar_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if e.control.value else ft.ThemeMode.LIGHT
        page.update()

    def confirmar_borrado(movimiento):
        def borrar(e):
            page.pop_dialog()
            try:
                repo.eliminar(movimiento.id)
                estado.value = "Movimiento eliminado"
                actualizar()
            except (ValueError, sqlite3.Error) as error:
                estado.value = f"No se eliminó: {error}"
                page.update()

        page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text("¿Eliminar este movimiento?"),
                content=ft.Text(f"{movimiento.concepto} · {moneda(movimiento.centavos)}"),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()),
                    ft.TextButton("Eliminar", on_click=borrar),
                ],
            )
        )

    for control in (concepto, importe, fecha, categoria, tipo):
        control.col = {"xs": 12, "md": 6}
    page.add(
        ft.Row(
            [
                ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=32), 
                ft.Text("Balance", size=36, weight=ft.FontWeight.BOLD),
                ft.Container(width= 450), 
                ft.Switch(label= 'Modo Oscuro', on_change= cambiar_tema)
            ],
            wrap=True,
        ),
        ft.Text("Controla entradas y salidas de efectivo · demostración local · MXN"),
        ft.Card(
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    [
                        ft.Text("Nuevo movimiento", size=22),
                        ft.ResponsiveRow([concepto, importe, fecha, categoria, tipo]),
                        ft.Button("Registrar movimiento", icon=ft.Icons.ADD, on_click=guardar),
                    ]
                ),
            )
        ),
        estado,
        ft.Divider(),
        ft.ResponsiveRow([filtro, filtro_tipo, mes]),
        ft.Button("Aplicar filtros", on_click=aplicar),
        alcance,
        resumen,
        ft.Text("Distribución por categoría", size=24),
        barras,
        ft.Text("Movimientos", size=24),
        vacio,
        ft.Row([tabla], scroll=ft.ScrollMode.AUTO),
        ft.Text("Datos locales de un usuario. No se conecta a cuentas bancarias.", size=12),
    )
    try:
        actualizar()
    except sqlite3.Error as error:
        estado.value = f"No se pudieron cargar los datos: {error}"
        page.update()


if __name__ == "__main__":
    ft.run(main)
