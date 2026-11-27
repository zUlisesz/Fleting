"""Renderiza los componentes sin abrir una ventana."""

import unittest

import flet as ft

from newton.analysis import Analysis, Line, analyze
from newton.main import App, ChartPanel, LogPanel, ProblemForm, main

from .render import render


def texts(controls) -> list[str]:
    return [c.value for c in controls if isinstance(c, ft.Text)]


class AppTests(unittest.TestCase):
    def test_initial_screen_invites_the_user_to_optimize(self):
        controls = render(App)

        shown = texts(controls)
        self.assertIn("Escribe una función y presiona Optimizar.", shown)
        self.assertIn("La gráfica aparecerá aquí.", shown)
        fields = [c for c in controls if isinstance(c, ft.TextField)]
        self.assertEqual([f.value for f in fields], ["(x-2)**4 + (x-2*y)**2", "0, 0"])
        self.assertFalse(next(c for c in controls if isinstance(c, ft.Button)).disabled)

    def test_main_is_callable(self):
        self.assertTrue(callable(main))


class PanelTests(unittest.TestCase):
    def test_log_panel_lists_lines_and_emphasizes_the_last(self):
        lines = (Line("Iteración 1: (1.0000, 2.0000)"), Line("Listo", "good"))

        entries = [c for c in render(LogPanel, lines) if isinstance(c, ft.Text)]

        self.assertEqual([t.value for t in entries][-2:], ["Iteración 1: (1.0000, 2.0000)", "Listo"])
        self.assertIsNone(entries[-2].weight)
        self.assertEqual(entries[-1].weight, ft.FontWeight.BOLD)
        self.assertEqual(entries[-1].color, ft.Colors.GREEN_700)

    def test_chart_panel_states(self):
        done = analyze("(x - 1)**2 + (y + 2)**2", "0, 0")
        failed = Analysis(Line("No se pudo optimizar: x", "error"))

        self.assertTrue(any(isinstance(c, ft.ProgressRing) for c in render(ChartPanel, None, True)))
        self.assertIn("La gráfica aparecerá aquí.", texts(render(ChartPanel, None, False)))
        self.assertIn("No se pudo generar la gráfica.", texts(render(ChartPanel, failed, False)))
        images = [c for c in render(ChartPanel, done, False) if isinstance(c, ft.Image)]
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0].src, done.image)

    def test_form_disables_the_button_while_running(self):
        def build(running: bool):
            noop = lambda *_: None
            return render(ProblemForm, "x**2 + y**2", "0, 0", running=running,
                          on_function_change=noop, on_point_change=noop, on_optimize=noop)

        button = lambda cs: next(c for c in cs if isinstance(c, ft.Button))
        self.assertFalse(button(build(False)).disabled)
        self.assertTrue(button(build(True)).disabled)


if __name__ == "__main__":
    unittest.main()
