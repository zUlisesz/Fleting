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


if __name__ == "__main__":
    unittest.main()
