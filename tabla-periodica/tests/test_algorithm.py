from pathlib import Path
import sys
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from algorithm import MAX_ATOMIC_NUMBER, calculate_chemistry_data


class ChemistryDataTests(unittest.TestCase):
    def test_calculates_data_for_the_last_supported_element(self):
        data = calculate_chemistry_data(MAX_ATOMIC_NUMBER)

        self.assertIsNotNone(data)
        self.assertIn("7p^6", data["configuration"])

    def test_rejects_values_outside_the_periodic_table(self):
        for atomic_number in (0, -1, MAX_ATOMIC_NUMBER + 1, True, 1.0):
            with self.subTest(atomic_number=atomic_number):
                self.assertIsNone(calculate_chemistry_data(atomic_number))


if __name__ == "__main__":
    unittest.main()
