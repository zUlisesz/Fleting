"""Gestor de archivos con Flet 1.0: UI declarativa (componentes + hooks).
    python3 main.py        # o: flet run main.py.  # o: flet run
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import flet as ft

from shell import Shell
from ui import (
    ConfirmDeleteDialog,
    EmptyState,
    EntryRow,
    Header,
    LocationBar,
    MUTED,
    NameDialog,
    Notice,
    SearchBar,
    Toast,
)

@dataclass(frozen=True)
class NewFolder:
    """Acción pendiente: crear una carpeta."""

@dataclass(frozen=True)
class Rename:
    name: str

@dataclass(frozen=True)
class Delete:
    name: str

@dataclass(frozen=True)
class Listing:
    """Resultado de leer la carpeta actual aplicando la búsqueda."""
    entries: list[Path]
    total: int
    error: str | None = None

def read_listing(shell: Shell, query: str) -> Listing:
    try:
        return Listing(shell.search(query), len(shell.ls()))
    except OSError as error:
        return Listing([], 0, str(error))

def status_text(listing: Listing, query: str) -> str:
    if listing.error:
        return "Error al cargar el contenido."
    count = len(listing.entries)
    noun = "elemento" if count == 1 else "elementos"
    if query.strip():
        return f"{count} de {listing.total} elementos coinciden con «{query.strip()}»"
    return f"{count} {noun}"

@ft.component
def App() -> ft.Control:
    shell, _ = ft.use_state(Shell)
    revision, set_revision = ft.use_state(0)  # sube tras cambiar el disco
    query, set_query = ft.use_state("")
    action, set_action = ft.use_state(None)  # NewFolder | Rename | Delete | None
    notice, set_notice = ft.use_state(None)

    listing = ft.use_memo(
        lambda: read_listing(shell, query), [shell.cwd, revision, query]
    )

    def refresh() -> None:
        set_revision(lambda r: r + 1)

    def notify(text: str, *, error: bool = False) -> None:
        set_notice(Notice(text, error))

    def close() -> None:
        set_action(None)

    def go(route: str) -> None:
        """Cambia de carpeta; la búsqueda se reinicia porque su alcance cambia."""
        try:
            shell.cd(route)
        except (OSError, ValueError) as error:
            notify(f"No se pudo abrir la carpeta: {error}", error=True)
            return
        set_query("")
        refresh()

    def go_up() -> None:
        if shell.can_go_up():
            go("..")
        else:
            notify("Ya estás en la carpeta inicial.")

    def create_folder(name: str) -> None:
        shell.mkdir(name)
        close()
        refresh()
        notify("Carpeta creada.")

    def rename(current: str, new: str) -> None:
        target = shell.rename(current, new)
        close()
        refresh()
        notify(f"Se renombró como {target.name}.")

    def delete(name: str) -> None:
        close()
        try:
            shell.rm(name)
        except (OSError, ValueError) as error:
            notify(f"No se pudo eliminar: {error}", error=True)
            return
        refresh()
        notify(f"Se eliminó {name}.")

    if listing.error:
        body: list[ft.Control] = [EmptyState(f"No se pudo leer esta carpeta: {listing.error}")]
    elif not listing.entries:
        empty = "Esta carpeta está vacía." if not query.strip() else "Sin resultados en esta carpeta."
        body = [EmptyState(empty)]
    else:
        body = [
            EntryRow(
                path,
                on_open=go,
                on_rename=lambda name: set_action(Rename(name)),
                on_delete=lambda name: set_action(Delete(name)),
                key=path.name,
            )
            for path in listing.entries
        ]

    overlay: ft.Control | None = None
    if isinstance(action, NewFolder):
        overlay = NameDialog(
            "Nueva carpeta",
            label="Nombre de la carpeta",
            confirm_label="Crear",
            on_submit=create_folder,
            on_close=close,
            key="new-folder",
        )
    elif isinstance(action, Rename):
        overlay = NameDialog(
            "Renombrar elemento",
            label="Nuevo nombre",
            confirm_label="Guardar",
            initial=action.name,
            on_submit=lambda new: rename(action.name, new),
            on_close=close,
            key=f"rename-{action.name}",
        )
    elif isinstance(action, Delete):
        overlay = ConfirmDeleteDialog(
            action.name,
            on_confirm=lambda: delete(action.name),
            on_close=close,
            key=f"delete-{action.name}",
        )

    return ft.Column(
        width=820,
        expand=True,
        spacing=16,
        controls=[
            Header(),
            ft.Card(
                expand=True,
                content=ft.Container(
                    padding=16,
                    expand=True,
                    content=ft.Column(
                        spacing=10,
                        expand=True,
                        controls=[
                            LocationBar(
                                str(shell.cwd),
                                can_go_up=shell.can_go_up(),
                                on_up=go_up,
                                on_refresh=refresh,
                            ),
                            SearchBar(
                                query,
                                on_change=set_query,
                                on_new_folder=lambda: set_action(NewFolder()),
                            ),
                            ft.Divider(),
                            ft.ListView(spacing=6, expand=True, controls=body),
                            ft.Text(status_text(listing, query), size=12, color=MUTED),
                        ],
                    ),
                ),
            ),
            # Diálogo y aviso: visibles solo mientras estén montados.
            *([overlay] if overlay else []),
            *([Toast(notice, on_dismiss=lambda: set_notice(None), key="toast")] if notice else []),
        ],
    )


def main(page: ft.Page) -> None:
    page.title = "Gestor de archivos"
    page.padding = 24
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.TEAL)
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 900
    page.window.height = 760
    page.window.min_width = 760
    page.window.min_height = 560
    page.render(App)


if __name__ == "__main__":
    ft.run(main)
