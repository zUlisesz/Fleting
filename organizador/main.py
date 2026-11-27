"""Organizador personal con Flet (UI imperativa).

    python3 -m organizador.main        # desde la carpeta que contiene `organizador/`
"""
import os
from pathlib import Path
import sqlite3
import flet as ft
from .modelo import PRIORIDADES, Repositorio


def main(page: ft.Page):
    page.title = "Enfoque · Organizador personal"
    page.padding = 24
    page.scroll = ft.ScrollMode.AUTO
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.theme_mode = ft.ThemeMode.LIGHT
    ruta = Path(os.environ.get("FLET_CURSO_DATA_DIR", str(Path.home() / ".flet_curso"))) / "organizador.sqlite3"
    try:
        repo = Repositorio(ruta)
    except (OSError, sqlite3.Error) as error:
        page.add(ft.Text(f"No se pudo abrir el almacenamiento: {error}"))
        return

    titulo = ft.TextField(label="¿Qué necesitas hacer?", hint_text="Ej. Preparar la práctica de Python", max_length=80)
    prioridad = ft.Dropdown(label="Prioridad", value="Media", options=[ft.DropdownOption(key=p, text=p) for p in PRIORIDADES])
    consulta = ft.TextField(label="Buscar tareas", prefix_icon=ft.Icons.SEARCH)
    filtro = ft.Dropdown(label="Mostrar", value="Todas", options=[ft.DropdownOption(key=x, text=x) for x in ("Todas", "Pendientes", "Completadas")])
    lista = ft.Column(spacing=8)
    metricas = ft.ResponsiveRow()
    progreso = ft.ProgressBar(value=0)
    resultado = ft.Text("Agrega tu primera tarea para comenzar.")
    edicion = None

    def tarjeta(nombre, valor):
        return ft.Container(col={"xs": 12, "sm": 4}, padding=18, border_radius=14,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            content=ft.Column([ft.Text(nombre), ft.Text(str(valor), size=30, weight=ft.FontWeight.BOLD)]))

    def refrescar():
        todas = repo.listar()
        completas = sum(t.completada for t in todas)
        metricas.controls = [tarjeta("Total", len(todas)), tarjeta("Pendientes", len(todas)-completas), tarjeta("Completadas", completas)]
        progreso.value = completas / len(todas) if todas else 0
        visibles = repo.listar(consulta.value or "", filtro.value)
        lista.controls = []
        for tarea in visibles:
            lista.controls.append(ft.Card(content=ft.Container(padding=12, content=ft.Row([
                ft.Checkbox(label=tarea.titulo, value=tarea.completada, expand=True,
                    on_change=lambda e, id=tarea.id: ejecutar(lambda: repo.completar(id, bool(e.control.value)), "Estado actualizado")),
                ft.Text(tarea.prioridad),
                ft.IconButton(ft.Icons.EDIT, tooltip="Editar tarea", on_click=lambda e, t=tarea: editar(t)),
                ft.IconButton(ft.Icons.DELETE_OUTLINE, tooltip="Eliminar tarea", on_click=lambda e, t=tarea: pedir_borrado(t)),
            ]))))
        if not visibles:
            lista.controls = [ft.Container(padding=24, content=ft.Text("No hay tareas para este filtro. Agrega una o cambia la búsqueda."))]
        page.update()

    def ejecutar(operacion, mensaje):
        try:
            operacion()
            resultado.value = mensaje
            refrescar()
            return True
        except (ValueError, sqlite3.Error, OSError) as error:
            resultado.value = f"No se completó la acción: {error}"
            page.update()
            return False

    def limpiar(e=None):
        nonlocal edicion
        edicion = None
        titulo.value = ""
        titulo.error = None
        prioridad.value = "Media"
        guardar.content = "Agregar tarea"
        cancelar.visible = False
        page.update()

    def guardar_tarea(e):
        if not 1 <= len((titulo.value or "").strip()) <= 80:
            titulo.error = "Escribe entre 1 y 80 caracteres."
            page.update()
            return
        titulo.error = None
        operacion = (lambda: repo.agregar(titulo.value, prioridad.value)) if edicion is None else (lambda: repo.editar(edicion, titulo.value, prioridad.value))
        if ejecutar(operacion, "Tarea guardada"):
            limpiar()

    def editar(tarea):
        nonlocal edicion
        edicion = tarea.id
        titulo.value = tarea.titulo
        prioridad.value = tarea.prioridad
        guardar.content = "Guardar cambios"
        cancelar.visible = True
        resultado.value = "Edita la tarea en el formulario superior."
        page.update()

    def pedir_borrado(tarea):
        def confirmar(e):
            page.pop_dialog()
            if ejecutar(lambda: repo.eliminar(tarea.id), "Tarea eliminada") and edicion == tarea.id:
                limpiar()
        page.show_dialog(ft.AlertDialog(modal=True, title=ft.Text("¿Eliminar tarea?"), content=ft.Text(tarea.titulo),
            actions=[ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()), ft.TextButton("Eliminar", on_click=confirmar)]))

    def cambiar_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if e.control.value else ft.ThemeMode.LIGHT
        page.update()

    guardar = ft.Button("Agregar tarea", icon=ft.Icons.ADD, on_click=guardar_tarea)
    cancelar = ft.TextButton("Cancelar edición", visible=False, on_click=limpiar)
    titulo.on_submit = guardar_tarea
    consulta.on_change = lambda e: ejecutar(lambda: None, "Filtro actualizado")
    filtro.on_select = lambda e: ejecutar(lambda: None, "Filtro actualizado")
    page.add(ft.Row([ft.Icon(ft.Icons.TASK_ALT, size=32), ft.Text("Enfoque", size=36, weight=ft.FontWeight.BOLD)], wrap=True),
        ft.Text("Tu plan, una tarea a la vez · demostración del curso"),
        ft.Switch(label="Modo oscuro", on_change=cambiar_tema), metricas,
        ft.Text("Progreso de todas tus tareas"), progreso,
        ft.Card(content=ft.Container(padding=20, content=ft.Column([ft.Text("Captura / edición", size=22), titulo, prioridad, ft.Row([guardar, cancelar], wrap=True)]))),
        resultado, consulta, filtro, lista,
        ft.Text("Persistencia local · un usuario · datos conservados al cerrar", size=12))
    ejecutar(lambda: None, "Listo")


if __name__ == "__main__":
    ft.run(main)
