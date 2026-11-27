"""Componente raíz: estado de la pantalla y coordinación con el repositorio."""

from __future__ import annotations

import sqlite3

import flet as ft

from .componentes import (
    ConfirmarBorrado,
    Distribucion,
    Encabezado,
    FormularioMovimiento,
    PanelFiltros,
    PanelResumen,
    SelectorPerfil,
    TablaMovimientos,
)
from .dominio import Filtros, Movimiento, resumir
from .repositorio import Repositorio

MENSAJE_INICIAL = "Registra tu primer movimiento. Todos los importes se expresan en MXN."
ERRORES = (ValueError, sqlite3.Error)


def cargar(repo: Repositorio, perfil_id: int, filtros: Filtros) -> tuple[list[Movimiento], str | None]:
    """Movimientos del perfil con los filtros, o ``([], error)`` si falla la base."""
    try:
        return repo.listar(perfil_id, filtros), None
    except ERRORES as error:
        return [], str(error)


@ft.component
def App(repo: Repositorio) -> ft.Control:
    perfil_id, set_perfil_id = ft.use_state(1)
    revision, set_revision = ft.use_state(0)  # sube al cambiar movimientos
    revision_perfiles, set_revision_perfiles = ft.use_state(0)
    filtros, set_filtros = ft.use_state(Filtros())
    estado, set_estado = ft.use_state(MENSAJE_INICIAL)
    por_borrar, set_por_borrar = ft.use_state(None)
    oscuro, set_oscuro = ft.use_state(False)

    perfiles = ft.use_memo(repo.perfiles, [repo, revision_perfiles])
    movimientos, error_carga = ft.use_memo(
        lambda: cargar(repo, perfil_id, filtros), [repo, perfil_id, filtros, revision]
    )
    resumen = ft.use_memo(lambda: resumir(movimientos), [movimientos])

    def actualizar() -> None:
        set_revision(lambda r: r + 1)

    def cambiar_tema(activo: bool) -> None:
        set_oscuro(activo)
        page = ft.context.page
        page.theme_mode = ft.ThemeMode.DARK if activo else ft.ThemeMode.LIGHT
        page.update()

    def seleccionar_perfil(nuevo: int) -> None:
        try:
            if not repo.existe_perfil(nuevo):
                raise ValueError("El perfil no existe.")
        except ERRORES as error:
            set_estado(f"No se pudo seleccionar el perfil: {error}")
            return
        set_perfil_id(nuevo)
        set_estado("Perfil seleccionado.")

    def crear_perfil(nombre: str) -> bool:
        try:
            nuevo = repo.crear_perfil(nombre)
        except ERRORES as error:
            set_estado(f"No se creó el perfil: {error}")
            return False
        set_revision_perfiles(lambda r: r + 1)
        set_perfil_id(nuevo)
        set_estado("Perfil seleccionado.")
        return True

    def guardar(fecha: str, concepto: str, categoria: str, tipo: str, importe: str) -> bool:
        try:
            repo.agregar(perfil_id, fecha, concepto, categoria, tipo, importe)
        except ERRORES as error:
            set_estado(f"No se guardó: {error}")
            return False
        set_estado("Movimiento guardado. Si no aparece, revisa los filtros activos.")
        actualizar()
        return True

    def aplicar_filtros(nuevos: Filtros) -> str | None:
        try:
            nuevos.validar()
        except ValueError as error:
            set_estado("Filtro no aplicado; se conservan los resultados anteriores.")
            return str(error)
        set_filtros(nuevos)
        set_estado("Filtros aplicados")
        return None

    def borrar() -> None:
        movimiento = por_borrar
        set_por_borrar(None)
        try:
            repo.eliminar(perfil_id, movimiento.id)
        except ERRORES as error:
            set_estado(f"No se eliminó: {error}")
            return
        set_estado("Movimiento eliminado")
        actualizar()

    return ft.SafeArea(
        content=ft.Column(
            controls=[
                Encabezado(oscuro=oscuro, on_tema=cambiar_tema),
                SelectorPerfil(
                    perfiles, perfil_id, on_seleccionar=seleccionar_perfil, on_crear=crear_perfil
                ),
                ft.Text("Controla entradas y salidas de efectivo · demostración local · MXN"),
                # ``key`` por perfil: al cambiar de perfil el formulario se reinicia.
                FormularioMovimiento(on_guardar=guardar, key=f"formulario-{perfil_id}"),
                ft.Text(estado),
                ft.Divider(),
                PanelFiltros(filtros, on_aplicar=aplicar_filtros),
                ft.Text(f"Resultados: {filtros.etiqueta}"),
                ft.Text(f"No se pudieron cargar los datos: {error_carga}", color=ft.Colors.RED_700,
                        visible=bool(error_carga)),
                PanelResumen(resumen),
                ft.Text("Distribución por categoría", size=24),
                Distribucion(resumen),
                ft.Text("Movimientos", size=24),
                TablaMovimientos(movimientos, on_eliminar=set_por_borrar),
                ft.Text("Perfiles locales sin contraseña. No se conecta a cuentas bancarias.", size=12),
                *(
                    [ConfirmarBorrado(por_borrar, on_confirmar=borrar,
                                      on_cancelar=lambda: set_por_borrar(None), key="borrar")]
                    if por_borrar
                    else []
                ),
            ]
        )
    )
