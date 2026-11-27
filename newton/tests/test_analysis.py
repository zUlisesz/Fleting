import unittest

from newton.analysis import Analysis, Line, analyze, iteration_log, status_line
from newton.optimizer import solve_newton
from newton.plotting import render_surface

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class AnalyzeTests(unittest.TestCase):
    def test_a_local_minimum_is_reported_as_good_with_a_chart(self):
        analysis = analyze("(x - 1)**2 + (y + 2)**2", "0, 0")

        self.assertFalse(analysis.failed)
        self.assertEqual(analysis.status, Line("Punto estacionario: mínimo local.", "good"))
        self.assertTrue(analysis.image.startswith(PNG_SIGNATURE))

    def test_other_stationary_points_are_warnings(self):
        analysis = analyze("x**2 - y**2", "0, 0")

        self.assertEqual(analysis.status.tone, "warning")
        self.assertIn("punto silla", analysis.status.text)
        self.assertEqual(analysis.log[-1].tone, "warning")

    def test_a_run_without_convergence_is_reported(self):
        analysis = analyze("x**4 + y**4", "10, 10")

        self.assertEqual(analysis.status, Line("Resultado generado sin convergencia.", "warning"))
        self.assertIn("sin cumplir la tolerancia", analysis.log[-1].text)
        self.assertFalse(analysis.failed)

    def test_invalid_input_becomes_an_error_analysis_instead_of_raising(self):
        cases = {
            "una sola variable": ("x**2", "0, 0"),
            "texto sin sentido": ("((", "0, 0"),
            "punto mal formado": ("x**2 + y**2", "1"),
            "punto no numérico": ("x**2 + y**2", "a, b"),
        }
        for name, (function, point) in cases.items():
            with self.subTest(name):
                analysis = analyze(function, point)

                self.assertTrue(analysis.failed)
                self.assertEqual(analysis.status.tone, "error")
                self.assertTrue(analysis.status.text.startswith("No se pudo optimizar: "))
                self.assertEqual(analysis.log, ())

    def test_a_singular_hessian_is_an_error_analysis(self):
        analysis = analyze("x**2 + y**4", "1, 0")  # Hessiana singular en (1, 0)

        self.assertTrue(analysis.failed)
        self.assertIn("Hessiana no es invertible", analysis.status.text)


class IterationLogTests(unittest.TestCase):
    def test_log_has_one_line_per_iteration_and_a_summary(self):
        result = solve_newton("(x - 1)**2 + (y + 2)**2", "0, 0")

        lines = iteration_log(result)

        self.assertEqual(len(lines), result.iterations + 1)
        self.assertTrue(lines[0].text.startswith("Iteración 1: ("))
        self.assertIn("Convergencia alcanzada", lines[-1].text)
        self.assertEqual(lines[-1].tone, "good")

    def test_status_line_matches_the_classification(self):
        result = solve_newton("-(x**2 + y**2)", "0, 0")

        self.assertEqual(status_line(result), Line("Punto estacionario: máximo local.", "warning"))


class RenderSurfaceTests(unittest.TestCase):
    def test_renders_a_png(self):
        result = solve_newton("(x - 1)**2 + (y + 2)**2", "0, 0")

        self.assertTrue(render_surface(result).startswith(PNG_SIGNATURE))

    def test_analysis_is_immutable(self):
        with self.assertRaises(AttributeError):
            Analysis(Line("x")).status = Line("y")  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
