from __future__ import annotations

import asyncio

import flet as ft

try:
    from .algoritmo import BOARD_SIZE, EMPTY, MoveResult, SudokuGame
except ImportError:  # Permite ejecutar: python main.py desde esta carpeta.
    from algoritmo import BOARD_SIZE, EMPTY, MoveResult, SudokuGame


CELL_SIZE = 60
MAX_ATTEMPTS = 3

GIVEN_COLOR = ft.Colors.BLUE_GREY_100
RELATED_COLOR = ft.Colors.LIGHT_BLUE_50
SELECTED_COLOR = ft.Colors.BLUE_200
WRONG_COLOR = ft.Colors.RED_100
WIN_COLOR = ft.Colors.LIGHT_GREEN_100


class SudokuApp:
    'coordina la presentación de Flet con el estado de una partida'

    def __init__(self, page: ft.Page):
        self.page = page
        self.game = SudokuGame.create(max_attempts=MAX_ATTEMPTS)
        self.cells: dict[tuple[int, int], ft.Container] = {}
        self.number_buttons: list[ft.Button] = []
        self.erase_button: ft.Button | None = None
        self.board_container: ft.Container | None = None
        self.timer_task = None

        self.timer_text = ft.Text(size=22, weight=ft.FontWeight.BOLD)
        self.attempts_text = ft.Text(size=16, weight=ft.FontWeight.BOLD)
        self.status_text = ft.Text("Selecciona una casilla vacía para comenzar.", size=15)
        self.restart_button = ft.Button(
            content="Jugar otra vez",
            icon=ft.Icons.RESTART_ALT,
            visible=False,
            on_click=self._restart_game,
        )

    def build(self) -> None:
        self.page.title = "Sudoku"
        self.page.padding = 24
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
        self.page.window.width = 720
        self.page.window.height = 860

        header = ft.Row(
            controls=[
                ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, size=34),
                ft.Column(
                    controls=[
                        ft.Text("Sudoku", size=32, weight=ft.FontWeight.BOLD),
                        ft.Text("Completa el tablero antes de agotar los intentos."),
                    ],
                    spacing=2,
                ),
            ],
            tight=True,
            spacing=12,
        )

        summary = ft.Row(
            controls=[
                self._stat_card("Tiempo", self.timer_text),
                self._stat_card("Intentos", self.attempts_text),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12,
            wrap=True,
        )

        self.board_container = ft.Container(
            content=self._build_board(),
            padding=6,
            border=ft.Border.all(2, ft.Colors.BLUE_GREY_700),
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
        )

        self.page.add(
            ft.Column(
                controls=[
                    header,
                    summary,
                    self.board_container,
                    self.status_text,
                    self.restart_button,
                    ft.Text("Números", size=18, weight=ft.FontWeight.BOLD),
                    self._build_keypad(),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16,
            )
        )
        self._refresh_view()
        self.timer_task = self.page.run_task(self._run_timer, self.game)

    def _stat_card(self, label: str, value: ft.Text) -> ft.Container:
        return ft.Container(
            content=ft.Column([ft.Text(label, size=13), value], spacing=2),
            padding=12,
            width=150,
            border_radius=10,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        )

    def _build_board(self) -> ft.Column:
        rows: list[ft.Row] = []
        for row in range(BOARD_SIZE):
            controls: list[ft.Container] = []
            for column in range(BOARD_SIZE):
                cell = ft.Container(
                    width=CELL_SIZE,
                    height=CELL_SIZE,
                    alignment=ft.Alignment.CENTER,
                    ink=True,
                    data=(row, column),
                    on_click=self._select_cell,
                    border=self._cell_border(row, column),
                    content=ft.Text(size=24, text_align=ft.TextAlign.CENTER),
                )
                self.cells[(row, column)] = cell
                controls.append(cell)
            rows.append(ft.Row(controls=controls, spacing=0, tight=True)) # type: ignore
        return ft.Column(controls=rows, spacing=0, tight=True) # type: ignore

    def _cell_border(self, row: int, column: int) -> ft.Border:
        thin = ft.BorderSide(width=0.5, color=ft.Colors.BLUE_GREY_300)
        thick = ft.BorderSide(width=2.5, color=ft.Colors.BLUE_GREY_700)
        return ft.Border.only(
            left=thick if column % 3 == 0 else thin,
            top=thick if row % 3 == 0 else thin,
            right=thick if column % 3 == 2 else None,
            bottom=thick if row % 3 == 2 else None,
        )

    def _build_keypad(self) -> ft.Row:
        controls: list[ft.Control] = []
        for value in range(1, BOARD_SIZE + 1):
            button = ft.Button(
                content=str(value),
                data=value,
                width=54,
                height=54,
                on_click=self._place_value,
                tooltip=f"Colocar {value}",
            )
            self.number_buttons.append(button)
            controls.append(button)
        self.erase_button = ft.Button(
            content="Del",
            icon=ft.Icons.DELETE_OUTLINE,
            width=96,
            height=54,
            on_click=self._erase_value,
        )
        controls.append(self.erase_button)
        return ft.Row(
            controls=controls,
            spacing=8,
            wrap=True,
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def _select_cell(self, event: ft.Event[ft.Container]) -> None:
        row, column = event.control.data
        result = self.game.select(row, column)
        self._show_result(result)

    def _place_value(self, event: ft.Event[ft.Button]) -> None:
        self._show_result(self.game.place(int(event.control.data)))

    def _erase_value(self, event: ft.Event[ft.Button]) -> None:
        self._show_result(self.game.erase_selected())

    def _restart_game(self, event: ft.Event[ft.Button]) -> None:
        if self.timer_task is not None:
            self.timer_task.cancel()

        self.game = SudokuGame.create(max_attempts=MAX_ATTEMPTS)
        self.cells.clear()
        if self.board_container is not None:
            self.board_container.content = self._build_board()

        self.status_text.value = "Nueva partida. Selecciona una casilla vacía para comenzar."
        self.status_text.color = None
        self._refresh_view()
        self.page.update()
        self.timer_task = self.page.run_task(self._run_timer, self.game)

    def _show_result(self, result: MoveResult) -> None:
        self.status_text.value = result.message
        self.status_text.color = (
            ft.Colors.GREEN_800 if result.won else ft.Colors.RED_800 if result.correct is False else None
        )
        self._refresh_view()
        self.page.update()

    def _refresh_view(self) -> None:
        self.timer_text.value = self._format_time(self.game.elapsed_seconds)
        self.attempts_text.value = f"{self.game.attempts} / {self.game.max_attempts}"

        for coordinate, cell in self.cells.items():
            row, column = coordinate
            value = self.game.board[row][column]
            cell.content.value = "" if value == EMPTY else str(value) #type: ignore
            cell.bgcolor = self._cell_color(row, column)
            cell.content.color = ft.Colors.BLUE_GREY_900 if coordinate in self.game.fixed_cells else ft.Colors.BLACK #type: ignore
            cell.content.weight = ft.FontWeight.BOLD if coordinate in self.game.fixed_cells else ft.FontWeight.NORMAL #type: ignore

        for button in self.number_buttons:
            button.disabled = self.game.finished
        if self.erase_button is not None:
            self.erase_button.disabled = self.game.finished
        self.restart_button.visible = self.game.finished

    def _cell_color(self, row: int, column: int):
        coordinate = (row, column)
        if self.game.finished and self.game.won:
            return WIN_COLOR
        if coordinate == self.game.selected:
            return SELECTED_COLOR
        if coordinate not in self.game.fixed_cells:
            value = self.game.board[row][column]
            if value != EMPTY and value != self.game.solution[row][column]:
                return WRONG_COLOR
        if self.game.selected and (row == self.game.selected[0] or column == self.game.selected[1]):
            return RELATED_COLOR
        if coordinate in self.game.fixed_cells:
            return GIVEN_COLOR
        return ft.Colors.WHITE

    async def _run_timer(self, game: SudokuGame) -> None:
        while self.game is game and not game.finished:
            await asyncio.sleep(1)
            if self.game is game and game.tick():
                self.timer_text.value = self._format_time(game.elapsed_seconds)
                self.timer_text.update()

    @staticmethod
    def _format_time(total_seconds: int) -> str:
        minutes, seconds = divmod(total_seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"


def main(page: ft.Page) -> None:
    app = SudokuApp(page)
    app.build()


if __name__ == "__main__":
    ft.run(main)
