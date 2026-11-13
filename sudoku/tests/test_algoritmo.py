import unittest

from sudoku.algoritmo import BOARD_SIZE, EMPTY, SudokuGame


def solved_board() -> list[list[int]]:
    return [
        [((row * 3 + row // 3 + column) % BOARD_SIZE) + 1 for column in range(BOARD_SIZE)]
        for row in range(BOARD_SIZE)
    ]


class SudokuGameTests(unittest.TestCase):
    def test_selecting_a_fixed_cell_keeps_the_previous_editable_selection(self):
        solution = solved_board()
        board = [row[:] for row in solution]
        board[0][0] = EMPTY
        fixed_cells = {
            (row, column)
            for row in range(BOARD_SIZE)
            for column in range(BOARD_SIZE)
            if (row, column) != (0, 0)
        }
        game = SudokuGame(solution=solution, board=board, fixed_cells=fixed_cells)

        game.select(0, 0)
        result = game.select(0, 1)
        placed = game.place(solution[0][0])

        self.assertTrue(result.accepted)
        self.assertEqual(game.selected, (0, 0))
        self.assertTrue(placed.correct)

    def test_rejects_non_integer_values_without_crashing(self):
        solution = solved_board()
        board = [row[:] for row in solution]
        board[0][0] = EMPTY
        game = SudokuGame(solution=solution, board=board, fixed_cells=set())
        game.select(0, 0)

        for value in (True, 1.0, "1", None):
            with self.subTest(value=value):
                result = game.place(value)

                self.assertFalse(result.accepted)
                self.assertEqual(game.board[0][0], EMPTY)


if __name__ == "__main__":
    unittest.main()
