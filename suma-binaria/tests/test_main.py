"""Renderiza los componentes sin abrir una ventana."""

import unittest

import flet as ft

from binario import sumar
from main import App, BinaryField, AdditionSheet, Equivalence, cell_size, main, strip_zeros, MAX_CELL, MIN_CELL

from .render import render


def texts(controls) -> list[str]:
    return [c.value for c in controls if isinstance(c, ft.Text)]


class HelpersTests(unittest.TestCase):
    def test_strip_zeros_keeps_at_least_one_digit(self):
        self.assertEqual(strip_zeros("0010"), "10")
        self.assertEqual(strip_zeros("000"), "0")
        self.assertEqual(strip_zeros("1"), "1")

    def test_cells_shrink_with_the_number_of_columns_within_limits(self):
        self.assertEqual(cell_size(3), MAX_CELL)
        self.assertLess(cell_size(17), cell_size(8))
        self.assertGreaterEqual(cell_size(500), MIN_CELL)


class AppTests(unittest.TestCase):
    def test_initial_screen_asks_for_two_numbers_and_the_clear_button_is_disabled(self):
        controls = render(App)

        self.assertIn("Escribe dos números binarios y el resultado aparece aquí.", texts(controls))
        fields = [c for c in controls if isinstance(c, ft.TextField)]
        self.assertEqual([f.label for f in fields], ["Primer número", "Segundo número"])
        self.assertTrue(next(c for c in controls if isinstance(c, ft.OutlinedButton)).disabled)

    def test_main_is_callable(self):
        self.assertTrue(callable(main))


class ComponentTests(unittest.TestCase):
    def test_binary_field_filters_everything_but_zeros_and_ones(self):
        field = next(c for c in render(BinaryField, "Primero", "10", on_change=lambda v: None)
                     if isinstance(c, ft.TextField))

        self.assertEqual(field.value, "10")
        self.assertEqual(field.input_filter.regex_string, "[01]")

    def test_addition_sheet_draws_operands_and_result(self):
        controls = render(AdditionSheet, sumar("101", "11"))

        shown = texts(controls)
        self.assertEqual(shown.count("+"), 1)
        # acarreos (tres 1) + 101 + 11 + resultado 1000, en el orden en que se dibujan
        self.assertEqual("".join(t for t in shown if t in ("0", "1")), "111" + "101" + "11" + "1000")
        self.assertIn("Acarreos", shown)

    def test_equivalence_shows_the_decimal_operation(self):
        self.assertIn("5 + 3 = 8", texts(render(Equivalence, sumar("101", "11"))))


if __name__ == "__main__":
    unittest.main()
