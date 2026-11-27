"""Componentes declarativos del gestor de archivos"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import flet as ft

from shell import describe

ACCENT = ft.Colors.TEAL_700
MUTED = ft.Colors.GREY_700


@dataclass(frozen=True)
class Notice:
    """Mensaje breve para el usuario (snackbar)."""

    text: str
    error: bool = False


@ft.component
def Header() -> ft.Control:
    return ft.Row(
        spacing=12,
        controls=[
            ft.Icon(ft.Icons.FOLDER_COPY_OUTLINED, size=32, color=ACCENT),
            ft.Column(
                spacing=2,
                controls=[
                    ft.Text("Gestor de archivos", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text("Explora y organiza tus carpetas locales."),
                ],
            ),
        ],
    )


@ft.component
def LocationBar(
    location: str,
    *,
    can_go_up: bool,
    on_up: Callable[[], None],
    on_refresh: Callable[[], None],
) -> ft.Control:
    """Ruta actual con botones para subir un nivel y actualizar."""
    return ft.Row(
        controls=[
            ft.IconButton(
                ft.Icons.ARROW_UPWARD_ROUNDED,
                tooltip="Subir un nivel",
                disabled=not can_go_up,
                on_click=lambda _: on_up(),
            ),
            ft.Column(
                spacing=2,
                expand=True,
                controls=[
                    ft.Text("Ubicación actual", size=12),
                    ft.Text(location, selectable=True),
                ],
            ),
            ft.IconButton(
                ft.Icons.REFRESH_ROUNDED,
                tooltip="Actualizar",
                on_click=lambda _: on_refresh(),
            ),
        ],
    )


@ft.component
def SearchBar(
    query: str,
    *,
    on_change: Callable[[str], None],
    on_new_folder: Callable[[], None],
) -> ft.Control:
    """Buscador por nombre (solo carpeta actual) y botón de nueva carpeta."""
    return ft.Row(
        spacing=12,
        controls=[
            ft.TextField(
                value=query,
                hint_text="Buscar en esta carpeta",
                helper="Solo busca entre los elementos de la carpeta actual",
                prefix_icon=ft.Icons.SEARCH,
                suffix=ft.IconButton(
                    ft.Icons.CLOSE,
                    tooltip="Limpiar búsqueda",
                    visible=bool(query),
                    on_click=lambda _: on_change(""),
                ),
                expand=True,
                dense=True,
                on_change=lambda e: on_change(e.control.value),
            ),
            ft.Button(
                "Nueva carpeta",
                icon=ft.Icons.CREATE_NEW_FOLDER_OUTLINED,
                on_click=lambda _: on_new_folder(),
            ),
        ],
    )


@ft.component
def EntryRow(
    path: Path,
    *,
    on_open: Callable[[str], None],
    on_rename: Callable[[str], None],
    on_delete: Callable[[str], None],
) -> ft.Control:
    """Fila de un archivo o carpeta con sus acciones."""
    is_directory = path.is_dir()
    return ft.Card(
        content=ft.Container(
            padding=ft.Padding.symmetric(horizontal=12, vertical=6),
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.FOLDER_ROUNDED if is_directory else ft.Icons.FILE_PRESENT_OUTLINED,
                        color=ACCENT,
                    ),
                    ft.Column(
                        spacing=2,
                        expand=True,
                        controls=[
                            ft.Text(path.name, weight=ft.FontWeight.W_600),
                            ft.Text(describe(path), size=12, color=MUTED),
                        ],
                    ),
                    ft.IconButton(
                        ft.Icons.EDIT_OUTLINED,
                        tooltip="Renombrar",
                        on_click=lambda _: on_rename(path.name),
                    ),
                    ft.IconButton(
                        ft.Icons.DELETE_OUTLINE,
                        tooltip="Eliminar",
                        on_click=lambda _: on_delete(path.name),
                    ),
                    ft.IconButton(
                        ft.Icons.ARROW_FORWARD_IOS_ROUNDED,
                        tooltip="Abrir carpeta" if is_directory else "No es una carpeta",
                        disabled=not is_directory,
                        on_click=lambda _: on_open(path.name),
                    ),
                ],
            ),
        )
    )


@ft.component
def EmptyState(message: str) -> ft.Control:
    return ft.Container(
        padding=20,
        alignment=ft.Alignment.CENTER,
        content=ft.Text(message, color=MUTED),
    )


# Diálogos
# Cada diálogo es un componente que se muestra mientras está montado
# (``ft.use_dialog``) y se cierra al desmontarse.

@ft.component
def NameDialog(
    title: str,
    *,
    label: str,
    confirm_label: str,
    on_submit: Callable[[str], None],
    on_close: Callable[[], None],
    initial: str = "",
) -> ft.Control:
    """Pide un nombre. ``on_submit`` puede lanzar ``OSError``/``ValueError``.
    El mensaje de la excepción se muestra bajo el campo y el diálogo sigue abierto.
    """
    text, set_text = ft.use_state(initial)
    error, set_error = ft.use_state(None)

    def submit(_=None) -> None:
        try:
            on_submit(text)
        except (OSError, ValueError) as exc:
            set_error(str(exc))

    ft.use_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text(title),
            content=ft.TextField(
                label=label,
                value=text,
                error=error,
                autofocus=True,
                on_change=lambda e: set_text(e.control.value),
                on_submit=submit,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: on_close()),
                ft.TextButton(confirm_label, on_click=submit),
            ],
        )
    )
    return ft.Container(visible=False)


@ft.component
def ConfirmDeleteDialog(
    name: str,
    *,
    on_confirm: Callable[[], None],
    on_close: Callable[[], None],
) -> ft.Control:
    ft.use_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text("¿Eliminar este elemento?"),
            content=ft.Text(f"{name}. La acción no se puede deshacer."),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: on_close()),
                ft.TextButton("Eliminar", on_click=lambda _: on_confirm()),
            ],
        )
    )
    return ft.Container(visible=False)


@ft.component
def Toast(notice: Notice, *, on_dismiss: Callable[[], None]) -> ft.Control:
    ft.use_dialog(
        ft.SnackBar(
            content=ft.Text(notice.text),
            bgcolor=ft.Colors.RED_700 if notice.error else ACCENT,
            on_dismiss=lambda _: on_dismiss(),
        )
    )
    return ft.Container(visible=False)
