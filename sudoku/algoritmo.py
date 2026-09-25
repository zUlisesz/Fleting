from __future__ import annotations

from dataclasses import dataclass, field
import random


BOARD_SIZE = 9
BOX_SIZE = 3
EMPTY = 0


def fill_matrix() -> list[list[int]]:
    solution = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def can_place(row: int, column: int, value: int) -> bool:
        if value in solution[row]:
            return False
        if any(solution[current_row][column] == value for current_row in range(BOARD_SIZE)):
            return False

        first_row = (row // BOX_SIZE) * BOX_SIZE
        first_column = (column // BOX_SIZE) * BOX_SIZE
        return all(
            solution[current_row][current_column] != value
            for current_row in range(first_row, first_row + BOX_SIZE)
            for current_column in range(first_column, first_column + BOX_SIZE)
        )

    def solve(position: int) -> bool:
        if position == BOARD_SIZE * BOARD_SIZE:
            return True

        row, column = divmod(position, BOARD_SIZE)
        candidates = list(range(1, BOARD_SIZE + 1))
        random.shuffle(candidates)
        for value in candidates:
            if can_place(row, column, value):
                solution[row][column] = value
                if solve(position + 1):
                    return True
                solution[row][column] = EMPTY
        return False

    if not solve(0):
        raise RuntimeError("No se pudo generar una solución de Sudoku.")
    return solution


def popmatrix(solution: list[list[int]], blanks_per_row: int = 5) -> list[list[int]]:
    if not 0 <= blanks_per_row <= BOARD_SIZE:
        raise ValueError("La cantidad de casillas vacías debe estar entre 0 y 9.")

    board = [row[:] for row in solution]
    for row in board:
        for column in random.sample(range(BOARD_SIZE), blanks_per_row):
            row[column] = EMPTY
    return board


def revisar_valor(respuestas: list[list[int]], value: int, row: int, column: int) -> bool:
    "indica si value coincide con la solución en una coordenada válida"
    if not (0 <= row < BOARD_SIZE and 0 <= column < BOARD_SIZE):
        return False
    return respuestas[row][column] == value


@dataclass(frozen=True)
class MoveResult:
    accepted: bool
    correct: bool | None
    message: str
    game_over: bool = False
    won: bool = False


@dataclass
class SudokuGame:
    'estado independiente de Flet para una partida de Sudoku'

    solution: list[list[int]]
    board: list[list[int]]
    max_attempts: int = 3
    attempts: int = 0
    elapsed_seconds: int = 0
    selected: tuple[int, int] | None = None
    finished: bool = False
    won: bool = False
    fixed_cells: set[tuple[int, int]] = field(default_factory=set)

    @classmethod
    def create(cls, max_attempts: int = 3, blanks_per_row: int = 5) -> "SudokuGame":
        if max_attempts < 1:
            raise ValueError("Debe permitirse al menos un intento.")
        solution = fill_matrix()
        board = popmatrix(solution, blanks_per_row)
        fixed_cells = {
            (row, column)
            for row in range(BOARD_SIZE)
            for column in range(BOARD_SIZE)
            if board[row][column] != EMPTY
        }
        return cls(solution=solution, board=board, max_attempts=max_attempts, fixed_cells=fixed_cells)

    @property
    def attempts_left(self) -> int:
        return self.max_attempts - self.attempts

    def select(self, row: int, column: int) -> MoveResult:
        if self.finished:
            return MoveResult(False, None, "La partida ya terminó.", game_over=True, won=self.won)
        if not (0 <= row < BOARD_SIZE and 0 <= column < BOARD_SIZE):
            return MoveResult(False, None, "La casilla seleccionada no es válida.")
        self.selected = (row, column)
        if (row, column) in self.fixed_cells:
            return MoveResult(True, None, "Esta casilla es una pista y no se puede editar.")
        return MoveResult(True, None, "Casilla seleccionada.")

    def place(self, value: int) -> MoveResult:
        if self.finished:
            return MoveResult(False, None, "La partida ya terminó.", game_over=True, won=self.won)
        if self.selected is None:
            return MoveResult(False, None, "Selecciona una casilla antes de elegir un número.")
        if not 1 <= value <= BOARD_SIZE:
            return MoveResult(False, None, "El valor debe estar entre 1 y 9.")

        row, column = self.selected
        if (row, column) in self.fixed_cells:
            return MoveResult(False, None, "Esta casilla es una pista y no se puede editar.")

        self.board[row][column] = value
        correct = revisar_valor(self.solution, value, row, column)
        if not correct:
            self.attempts += 1
            if self.attempts >= self.max_attempts:
                self.finished = True
                return MoveResult(True, False, "Se agotaron los intentos.", game_over=True)
            return MoveResult(True, False, f"Valor incorrecto. Quedan {self.attempts_left} intentos.")

        if self.board == self.solution:
            self.finished = True
            self.won = True
            return MoveResult(True, True, "¡Sudoku completado!", game_over=True, won=True)
        return MoveResult(True, True, "Valor correcto.")

    def erase_selected(self) -> MoveResult:
        if self.finished:
            return MoveResult(False, None, "La partida ya terminó.", game_over=True, won=self.won)
        if self.selected is None:
            return MoveResult(False, None, "Selecciona una casilla antes de borrar.")

        row, column = self.selected
        if (row, column) in self.fixed_cells:
            return MoveResult(False, None, "Esta casilla es una pista y no se puede borrar.")
        self.board[row][column] = EMPTY
        return MoveResult(True, None, "Casilla borrada.")

    def tick(self) -> bool:
        'avanza el temporizador y devuelve si la partida continúa'
        if self.finished:
            return False
        self.elapsed_seconds += 1
        return True
