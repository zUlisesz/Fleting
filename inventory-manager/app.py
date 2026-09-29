"""Flet desktop interface for inventory workbooks with the same XLSX columns."""

from __future__ import annotations

from pathlib import Path
from zipfile import BadZipFile

import flet as ft
from openpyxl.utils.exceptions import InvalidFileException

from scrip import DEFAULT_FILE, INVENTORY_HEADERS, ExcelAPI


PAGE_SIZE = 25
SEARCH_COLUMNS = ("Código", "Producto", "Departamento")
DEFAULT_VALUES = {
    "P. Costo": "$0.00",
    "P. Venta": "$0.00",
    "P. Mayoreo": "$0.00",
    "Departamento": "- Sin Departamento -",
    "Existencia": "0",
    "Inv. Mínimo": "0",
    "Inv. Máximo": "0",
    "Tipo de Venta": "UNIDAD",
}
WORKBOOK_ERRORS = (OSError, ValueError, KeyError, BadZipFile, InvalidFileException)


class InventoryApp:
    """Keep Flet controls separate from XLSX access in :class:`ExcelAPI`."""

    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.api: ExcelAPI | None = None
        self.records: list[dict] = []
        self.filtered: list[dict] = []
        self.page_number = 0
        self.picker = ft.FilePicker()
        page.services.append(self.picker)

        self.file_input = ft.TextField(
            label="Archivo XLSX",
            value=str(DEFAULT_FILE),
            helper="Escribe la ruta de un inventario o selecciónalo con Examinar.",
            on_submit=self.load_file,
            col={"xs": 12, "md": 8},
        )
        self.active_file = ft.Text("Ningún archivo cargado", selectable=True)
        self.status = ft.Text("Selecciona un archivo XLSX para comenzar.")
        self.search_input = ft.TextField(
            label="Buscar",
            hint_text="Código, producto o departamento",
            on_submit=self.apply_filters,
            col={"xs": 12, "md": 7},
        )
        self.department = ft.Dropdown(
            label="Departamento",
            value="Todos",
            options=[ft.DropdownOption(key="Todos", text="Todos")],
            on_select=self.apply_filters,
            col={"xs": 12, "md": 5},
        )
        self.total_count = ft.Text("0", size=28, weight=ft.FontWeight.BOLD)
        self.match_count = ft.Text("0", size=28, weight=ft.FontWeight.BOLD)
        self.page_label = ft.Text("Página 0 de 0")
        self.empty_message = ft.Text("No hay productos para mostrar.")
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text(label))
                for label in (
                    "Código",
                    "Producto",
                    "Departamento",
                    "Existencia",
                    "P. Costo", 
                    "P. Venta",
                    "Tipo de Venta",
                    "Acciones",
                )
            ],
            rows=[],
            column_spacing=22,
        )
        self.previous_button = ft.Button("Anterior", on_click=self.previous_page, disabled=True)
        self.next_button = ft.Button("Siguiente", on_click=self.next_page, disabled=True)
        self.add_button = ft.Button(
            "Agregar producto", icon=ft.Icons.ADD, on_click=self.open_add, disabled=True
        )

    def build(self) -> None:
        page = self.page
        page.title = "Inventario XLSX"
        page.padding = 24
        page.scroll = ft.ScrollMode.AUTO
        page.window.width = 1220
        page.window.height = 860
        page.theme = ft.Theme(color_scheme_seed=ft.Colors.TEAL)
        page.theme_mode = ft.ThemeMode.LIGHT

        page.add(
            ft.Row(
                [
                    ft.Icon(ft.Icons.INVENTORY_2, size=32, color=ft.Colors.TEAL_700),
                    ft.Text("Inventario", size=34, weight=ft.FontWeight.BOLD),
                ],
                spacing=12,
            ),
            ft.Text("Consulta y edita productos del archivo XLSX seleccionado."),
            ft.Card(
                content=ft.Container(
                    padding=18,
                    content=ft.Column(
                        [
                            ft.Text("Archivo de trabajo", size=21, weight=ft.FontWeight.BOLD),
                            ft.ResponsiveRow(
                                [
                                    self.file_input,
                                    ft.Button(
                                        "Examinar",
                                        icon=ft.Icons.FOLDER_OPEN,
                                        on_click=self.choose_file,
                                        col={"xs": 6, "md": 2},
                                    ),
                                    ft.Button(
                                        "Cargar",
                                        icon=ft.Icons.REFRESH,
                                        on_click=self.load_file,
                                        col={"xs": 6, "md": 2},
                                    ),
                                ]
                            ),
                            self.active_file,
                        ],
                        spacing=12,
                    ),
                )
            ),
            self.status,
            ft.ResponsiveRow(
                [
                    self._summary_card("Productos en el archivo", self.total_count),
                    self._summary_card("Resultados del filtro", self.match_count),
                ]
            ),
            ft.Row([ft.Text("Productos", size=24, weight=ft.FontWeight.BOLD), self.add_button]),
            ft.ResponsiveRow([self.search_input, self.department]),
            ft.Button("Aplicar búsqueda", icon=ft.Icons.SEARCH, on_click=self.apply_filters),
            self.empty_message,
            ft.Row([self.table], scroll=ft.ScrollMode.AUTO),
            ft.Row([self.previous_button, self.page_label, self.next_button], spacing=14),
        )
        self.load_file()

    @staticmethod
    def _summary_card(title: str, value: ft.Text) -> ft.Container:
        return ft.Container(
            col={"xs": 12, "sm": 6},
            padding=18,
            border_radius=14,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            content=ft.Column([ft.Text(title), value], spacing=4),
        )

    def _show_status(self, message: str, *, error: bool = False) -> None:
        self.status.value = message
        self.status.color = ft.Colors.RED_700 if error else ft.Colors.GREEN_700
        self.page.update()

    async def choose_file(self, event: ft.ControlEvent) -> None:
        files = await self.picker.pick_files(
            dialog_title="Seleccionar inventario XLSX",
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["xlsx"],
            allow_multiple=False,
        )
        if not files:
            return
        if not files[0].path:
            self._show_status("No se recibió una ruta local. Escríbela en Archivo XLSX.", error=True)
            return
        self.file_input.value = files[0].path
        self.load_file()

    def load_file(
        self, event: ft.ControlEvent | None = None, *, preserve_filters: bool = False
    ) -> None:
        raw_path = (self.file_input.value or "").strip()
        if not raw_path:
            self._show_status("Indica la ruta de un archivo XLSX.", error=True)
            return
        path = Path(raw_path).expanduser()
        if path.suffix.lower() != ".xlsx":
            self._show_status("Selecciona un archivo con extensión .xlsx.", error=True)
            return

        candidate: ExcelAPI | None = None
        try:
            candidate = ExcelAPI(path, expected_headers=INVENTORY_HEADERS)
            records = candidate.get_all()
        except WORKBOOK_ERRORS as error:
            if candidate is not None:
                candidate.close()
            self._show_status(f"No se pudo cargar el archivo: {error}", error=True)
            return

        current_search = (self.search_input.value or "") if preserve_filters else ""
        current_department = (self.department.value or "Todos") if preserve_filters else "Todos"
        if self.api is not None:
            self.api.close()
        self.api = candidate
        self.records = records
        self.file_input.value = str(candidate.filepath.resolve())
        self.file_input.error = None
        self.active_file.value = f"Archivo activo: {candidate.filepath.resolve()}"
        self.search_input.value = current_search
        self.department.options = [ft.DropdownOption(key="Todos", text="Todos")]
        self.department.options.extend(
            ft.DropdownOption(key=name, text=name)
            for name in sorted({str(row["Departamento"]) for row in records if row["Departamento"]})
            if name != "Todos"
        )
        department_keys = {option.key for option in self.department.options}
        self.department.value = (
            current_department if current_department in department_keys else "Todos"
        )
        self.add_button.disabled = False
        self.page_number = 0
        self.apply_filters()
        self._show_status(f"Archivo cargado: {candidate.filepath.name} ({len(records)} productos).")

    def apply_filters(self, event: ft.ControlEvent | None = None) -> None:
        if self.api is None:
            return
        query = (self.search_input.value or "").strip()
        rows = self.api.search(query, columns=SEARCH_COLUMNS) if query else self.api.get_all()
        selected_department = self.department.value or "Todos"
        if selected_department != "Todos":
            rows = [row for row in rows if row["Departamento"] == selected_department]
        self.filtered = rows
        self.page_number = 0
        self._render_table()

    def _render_table(self) -> None:
        total_pages = (len(self.filtered) + PAGE_SIZE - 1) // PAGE_SIZE
        self.page_number = min(self.page_number, max(total_pages - 1, 0))
        start = self.page_number * PAGE_SIZE
        visible_rows = self.filtered[start : start + PAGE_SIZE]
        self.table.rows = [self._table_row(record) for record in visible_rows]
        self.table.visible = bool(visible_rows)
        self.empty_message.visible = not bool(visible_rows)
        self.total_count.value = str(len(self.records))
        self.match_count.value = str(len(self.filtered))
        self.page_label.value = (
            f"Página {self.page_number + 1} de {total_pages}" if total_pages else "Página 0 de 0"
        )
        self.previous_button.disabled = self.page_number == 0
        self.next_button.disabled = self.page_number + 1 >= total_pages
        self.page.update()

    def _table_row(self, record: dict) -> ft.DataRow:
        code = record["Código"]
        cells = [
            ft.DataCell(
                ft.Text("" if record[column] is None else str(record[column]), max_lines=2)
            )
            for column in (
                "Código",
                "Producto",
                "Departamento",
                "Existencia",
                "P. Costo",
                "P. Venta",
                "Tipo de Venta",
            )
        ]
        cells.append(
            ft.DataCell(
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.EDIT_OUTLINED,
                            tooltip="Editar producto",
                            on_click=lambda event, item=record: self.open_edit(item),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            tooltip="Eliminar producto",
                            on_click=lambda event, item=record: self.confirm_delete(item),
                        ),
                    ],
                    spacing=0,
                )
            )
        )
        return ft.DataRow(cells=cells, key=str(code))

    def previous_page(self, event: ft.ControlEvent) -> None:
        if self.page_number > 0:
            self.page_number -= 1
            self._render_table()

    def next_page(self, event: ft.ControlEvent) -> None:
        if (self.page_number + 1) * PAGE_SIZE < len(self.filtered):
            self.page_number += 1
            self._render_table()

    def open_add(self, event: ft.ControlEvent) -> None:
        self._open_form()

    def open_edit(self, record: dict) -> None:
        self._open_form(record)

    def _open_form(self, original: dict | None = None) -> None:
        if self.api is None:
            return
        editing = original is not None
        fields = {
            header: ft.TextField(
                label=header,
                value=(
                    "" if original[header] is None else str(original[header])
                ) if editing else DEFAULT_VALUES.get(header, ""),
                read_only=editing and header == "Código",
                col={"xs": 12, "sm": 6},
            )
            for header in INVENTORY_HEADERS
        }
        form_error = ft.Text(color=ft.Colors.RED_700)

        def submit(event: ft.ControlEvent) -> None:
            values = {name: (field.value or "").strip() for name, field in fields.items()}
            if not values["Código"] or not values["Producto"]:
                form_error.value = "Código y Producto son obligatorios."
                self.page.update()
                return

            def change(working: ExcelAPI) -> None:
                if editing:
                    changes = {name: value for name, value in values.items() if name != "Código"}
                    if working.update_by_code(original["Código"], changes) != 1:
                        raise ValueError("El producto ya no existe o el código está duplicado.")
                else:
                    working.add(values)

            try:
                self._commit(change)
            except WORKBOOK_ERRORS as error:
                form_error.value = str(error)
                self.page.update()
                return
            self.page.pop_dialog()
            self._show_status("Producto actualizado." if editing else "Producto agregado.")

        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text("Editar producto" if editing else "Agregar producto"),
                content=ft.Container(
                    width=730,
                    height=340,
                    content=ft.Column(
                        [ft.ResponsiveRow(list(fields.values())), form_error],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                ),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda event: self.page.pop_dialog()),
                    ft.Button("Guardar", icon=ft.Icons.SAVE, on_click=submit),
                ],
            )
        )

    def confirm_delete(self, record: dict) -> None:
        if self.api is None:
            return

        def delete(event: ft.ControlEvent) -> None:
            try:
                def change(working: ExcelAPI) -> None:
                    if working.delete_by_code(record["Código"]) != 1:
                        raise ValueError("El producto ya no existe o el código está duplicado.")

                self._commit(change)
            except WORKBOOK_ERRORS as error:
                self.page.pop_dialog()
                self._show_status(f"No se eliminó: {error}", error=True)
                return
            self.page.pop_dialog()
            self._show_status("Producto eliminado.")

        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text("¿Eliminar producto?"),
                content=ft.Text(f"{record['Código']} · {record['Producto']}"),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda event: self.page.pop_dialog()),
                    ft.TextButton("Eliminar", on_click=delete),
                ],
            )
        )

    def _commit(self, change) -> None:
        """Apply one change to a fresh copy and persist it before updating the UI."""
        if self.api is None:
            raise ValueError("No hay ningún archivo cargado.")
        path = self.api.filepath
        with ExcelAPI(path, expected_headers=INVENTORY_HEADERS) as working:
            change(working)
            working.save()
        self.file_input.value = str(path)
        self.load_file(preserve_filters=True)


def main(page: ft.Page) -> None:
    InventoryApp(page).build()


if __name__ == "__main__":
    ft.run(main)
