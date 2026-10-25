import unittest
from unittest.mock import patch

from cajero.model import Cajero


class CajeroTests(unittest.TestCase):
    def test_successful_withdrawal_returns_bills_and_reduces_balance(self):
        cajero = Cajero()

        with patch("cajero.model.random.choices", side_effect=[[100], [100]]):
            bills = cajero.entregar_dinero(200)

        self.assertEqual(bills, [100, 100])
        self.assertEqual(cajero.dinero, 49_800)

    def test_invalid_withdrawals_return_no_bills_and_preserve_balance(self):
        for amount in (50, 150, 6_100):
            with self.subTest(amount=amount):
                cajero = Cajero()
                bills = cajero.entregar_dinero(amount)

                self.assertEqual(bills, [])
                self.assertEqual(cajero.dinero, 50_000)

    def test_withdrawal_over_available_balance_is_rejected(self):
        cajero = Cajero()
        cajero.dinero = 100

        bills = cajero.entregar_dinero(200)

        self.assertEqual(bills, [])
        self.assertEqual(cajero.dinero, 100)

    def test_minimum_valid_withdrawal_is_one_hundred(self):
        cajero = Cajero()

        with patch("cajero.model.random.choices", return_value=[100]):
            bills = cajero.entregar_dinero(100)

        self.assertEqual(bills, [100])
        self.assertEqual(cajero.dinero, 49_900)


if __name__ == "__main__":
    unittest.main()
