import unittest

from newton.optimizer import (
    LOCAL_MAXIMUM,
    LOCAL_MINIMUM,
    SADDLE_OR_FLAT_POINT,
    solve_newton,
)


class SolveNewtonTests(unittest.TestCase):
    def test_classifies_a_local_minimum(self):
        result = solve_newton("(x - 1)**2 + (y + 2)**2", "0, 0")

        self.assertTrue(result.converged)
        self.assertEqual(result.stationary_point_type, LOCAL_MINIMUM)

    def test_classifies_a_local_maximum(self):
        result = solve_newton("-(x**2 + y**2)", "0, 0")

        self.assertTrue(result.converged)
        self.assertEqual(result.stationary_point_type, LOCAL_MAXIMUM)

    def test_classifies_a_saddle_point(self):
        result = solve_newton("x**2 - y**2", "0, 0")

        self.assertTrue(result.converged)
        self.assertEqual(result.stationary_point_type, SADDLE_OR_FLAT_POINT)

    def test_rejects_invalid_solver_parameters(self):
        for tolerance in (0, -1, float("inf"), True):
            with self.subTest(tolerance=tolerance):
                with self.assertRaises(ValueError):
                    solve_newton("x**2 + y**2", "0, 0", tolerance=tolerance)

        for max_iterations in (0, -1, 1.0, True):
            with self.subTest(max_iterations=max_iterations):
                with self.assertRaises(ValueError):
                    solve_newton("x**2 + y**2", "0, 0", max_iterations=max_iterations)


if __name__ == "__main__":
    unittest.main()
