from __future__ import annotations

import flet as ft

try:
    from .back import Shell
except ImportError:  # Permite ejecutar: python app.py desde esta carpeta.
    from back import Shell


class FileManagerApp:
    """Connects the Flet controls to the filesystem browser."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.browser = Shell()
        self.entries = ft.ListView(spacing=6, height=520)
        self.location = ft.Text(selectable=True)
        self.status = ft.Text(size=12, color=ft.Colors.GREY_700)

    def build(self) -> None:
        self.page.title = "Gestor de archivos"
        self.page.padding = 24
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.theme = ft.Theme(color_scheme_seed=ft.Colors.TEAL)
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.window.width = 900
        self.page.window.height = 760
        self.page.window.min_width = 760
        self.page.window.min_height = 560

        header = ft.Row(
            controls=[
                ft.Icon(ft.Icons.FOLDER_COPY_OUTLINED, size=32, color=ft.Colors.TEAL_700),
                ft.Column(
                    controls=[
                        ft.Text("Gestor de archivos", size=30, weight=ft.FontWeight.BOLD),
                        ft.Text("Explora y organiza tus carpetas locales."),
                    ],
                    spacing=2,
                ),
            ],
            spacing=12,
        )
        actions = ft.Row(
            controls=[
                ft.Button(
                    "Nueva carpeta",
                    icon=ft.Icons.CREATE_NEW_FOLDER_OUTLINED,
                    on_click=self._create_folder,
                )
            ],
            alignment=ft.MainAxisAlignment.END,
        )
        location_bar = ft.Row(
            controls=[
                ft.IconButton(
                    ft.Icons.ARROW_UPWARD_ROUNDED,
                    tooltip="Subir un nivel",
                    on_click=self._go_up,
                ),
                ft.Column(
                    controls=[ft.Text("Ubicación actual", size=12), self.location],
                    spacing=2,
                    expand=True,
                ),
                ft.IconButton(
                    ft.Icons.REFRESH_ROUNDED,
                    tooltip="Actualizar",
                    on_click=lambda _: self._refresh(),
                ),
            ],
        )
        self.page.add(
            ft.Column(
                width=820,
                controls=[
                    header,
                    actions,
                    ft.Card(
                        content=ft.Container(
                            padding=16,
                            content=ft.Column(
                                controls=[
                                    location_bar,
                                    ft.Divider(),
                                    self.entries,
                                    self.status,
                                ],
                                spacing=10,
                                width=780,
                            ),
                            width=820,
                        )
                    ),
                ],
                spacing=16,
            )
        )
        self._refresh()

    def _refresh(self) -> None:
        self.location.value = str(self.browser.cwd)
        try:
            items = self.browser.ls()
        except OSError as error:
            self.entries.controls = [ft.Text(f"No se pudo leer esta carpeta: {error}")]
            self.status.value = "Error al cargar el contenido."
            self.page.update()
            return

        self.entries.controls = [self._entry(item) for item in items]
        if not items:
            self.entries.controls = [
                ft.Container(
                    padding=20,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text("Esta carpeta está vacía."),
                )
            ]
        self.status.value = f"{len(items)} elemento" + ("s" if len(items) != 1 else "")
        self.page.update()

    def _entry(self, path) -> ft.Control:
        is_directory = path.is_dir()
        try:
            description = "Carpeta" if is_directory else f"{path.stat().st_size:,} bytes"
        except OSError:
            description = "No disponible"
        icon = ft.Icons.FOLDER_ROUNDED if is_directory else ft.Icons.FILE_PRESENT_OUTLINED
        return ft.Card(
            content=ft.Container(
                padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                content=ft.Row(
                    controls=[
                        ft.Icon(icon, color=ft.Colors.TEAL_700),
                        ft.Column(
                            controls=[
                                ft.Text(path.name, weight=ft.FontWeight.W_600),
                                ft.Text(description, size=12, color=ft.Colors.GREY_700),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            tooltip="Eliminar",
                            on_click=lambda _: self._confirm_delete(path.name),
                        ),
                        ft.IconButton(
                            ft.Icons.ARROW_FORWARD_IOS_ROUNDED,
                            tooltip="Abrir carpeta" if is_directory else "No es una carpeta",
                            disabled=not is_directory,
                            on_click=lambda _: self._enter_folder(path.name),
                        ),
                    ],
                ),
            )
        )

    def _enter_folder(self, name: str) -> None:
        try:
            self.browser.cd(name)
            self._refresh()
        except (OSError, ValueError) as error:
            self._notify(f"No se pudo abrir la carpeta: {error}", error=True)

    def _go_up(self, _: ft.ControlEvent) -> None:
        if self.browser.cwd.parent == self.browser.cwd:
            self._notify("Ya estás en la carpeta raíz.")
            return
        self.browser.cd("..")
        self._refresh()

    def _create_folder(self, _: ft.ControlEvent) -> None:
        name = ft.TextField(label="Nombre de la carpeta", autofocus=True)

        def save(_: ft.ControlEvent) -> None:
            try:
                self.browser.mkdir(name.value or "")
                self.page.pop_dialog()
                self._refresh()
                self._notify("Carpeta creada.")
            except (OSError, ValueError) as error:
                name.error_text = str(error)
                self.page.update()

        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text("Nueva carpeta"),
                content=name,
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda _: self.page.pop_dialog()),
                    ft.TextButton("Crear", on_click=save),
                ],
            )
        )

    def _confirm_delete(self, name: str) -> None:
        def delete(_: ft.ControlEvent) -> None:
            self.page.pop_dialog()
            try:
                self.browser.rm(name)
                self._refresh()
                self._notify(f"Se eliminó {name}.")
            except (OSError, ValueError) as error:
                self._notify(f"No se pudo eliminar: {error}", error=True)

        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text("¿Eliminar este elemento?"),
                content=ft.Text(f"{name}. La acción no se puede deshacer."),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda _: self.page.pop_dialog()),
                    ft.TextButton("Eliminar", on_click=delete),
                ],
            )
        )

    def _notify(self, message: str, error: bool = False) -> None:
        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.Colors.RED_700 if error else ft.Colors.TEAL_700,
            )
        )


def main(page: ft.Page) -> None:
    FileManagerApp(page).build()


if __name__ == "__main__":
    ft.run(main)
