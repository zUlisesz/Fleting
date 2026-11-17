from pathlib import Path
import sys
import unittest
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from algorithm import MAX_ATOMIC_NUMBER, ORBITAL_EXCEPTIONS, calculate_chemistry_data


class ChemistryDataTests(unittest.TestCase):
    def test_calculates_data_for_the_last_supported_element(self):
        data = calculate_chemistry_data(MAX_ATOMIC_NUMBER)

        self.assertIsNotNone(data)
        self.assertIn("7p^6", data["configuration"])

    def test_rejects_values_outside_the_periodic_table(self):
        for atomic_number in (0, -1, MAX_ATOMIC_NUMBER + 1, True, 1.0):
            with self.subTest(atomic_number=atomic_number):
                self.assertIsNone(calculate_chemistry_data(atomic_number))

    def test_uses_known_chromium_and_copper_orbital_exceptions(self):
        chromium = calculate_chemistry_data(24)
        copper = calculate_chemistry_data(29)

        self.assertTrue(chromium["configuration"].endswith("4s^1 3d^5"))
        self.assertTrue(copper["configuration"].endswith("4s^1 3d^10"))

    def test_uses_known_exceptions_in_the_five_s_and_four_d_orbitals(self):
        niobium = calculate_chemistry_data(41)
        palladium = calculate_chemistry_data(46)
        silver = calculate_chemistry_data(47)

        self.assertTrue(niobium["configuration"].endswith("5s^1 4d^4"))
        self.assertTrue(palladium["configuration"].endswith("5s^0 4d^10"))
        self.assertTrue(silver["configuration"].endswith("5s^1 4d^10"))

    def test_uses_known_exceptions_in_the_six_s_and_five_d_orbitals(self):
        platinum = calculate_chemistry_data(78)
        gold = calculate_chemistry_data(79)

        self.assertTrue(platinum["configuration"].endswith("6s^1 4f^14 5d^9"))
        self.assertTrue(gold["configuration"].endswith("6s^1 4f^14 5d^10"))

    def test_uses_known_gadolinium_orbital_exception(self):
        gadolinium = calculate_chemistry_data(64)

        self.assertTrue(gadolinium["configuration"].endswith("6s^2 4f^7 5d^1"))

    def test_rejects_an_exception_that_changes_the_electron_total(self):
        with patch.dict(ORBITAL_EXCEPTIONS, {24: {"4s": 2, "3d": 5}}):
            self.assertIsNone(calculate_chemistry_data(24))


if __name__ == "__main__":
    unittest.main()
