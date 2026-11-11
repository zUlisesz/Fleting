import unittest

from cajero.model import Cajero


class CajeroTests(unittest.TestCase):
    def test_successful_withdrawal_returns_bills_and_reduces_balance(self):
        cajero = Cajero()

        bills = cajero.entregar_dinero(200)

        self.assertEqual(bills, [200])
        self.assertEqual(cajero.dinero, 49_800)

    def test_invalid_withdrawals_return_no_bills_and_preserve_balance(self):
        for amount in (50, 150, 6_100):
            with self.subTest(amount=amount):
                cajero = Cajero()
                bills = cajero.entregar_dinero(amount)

                self.assertEqual(bills, [])
                self.assertEqual(cajero.dinero, 50_000)

    def test_withdrawal_message_matches_the_authorization_result(self):
        cajero = Cajero()

        message, authorized = cajero.mensaje_retiro(200)

        self.assertTrue(authorized)
        self.assertEqual(message, "Retiro por $ 200 exitoso")

    def test_withdrawal_over_available_balance_is_rejected(self):
        cajero = Cajero()
        cajero.dinero = 100

        bills = cajero.entregar_dinero(200)

        self.assertEqual(bills, [])
        self.assertEqual(cajero.dinero, 100)

    def test_minimum_valid_withdrawal_is_one_hundred(self):
        cajero = Cajero()

        bills = cajero.entregar_dinero(100)

        self.assertEqual(bills, [100])
        self.assertEqual(cajero.dinero, 49_900)

    def test_every_authorized_withdrawal_is_delivered_exactly(self):
        for amount in range(100, 6_001, 100):
            with self.subTest(amount=amount):
                cajero = Cajero()

                bills = cajero.entregar_dinero(amount)

                self.assertEqual(sum(bills), amount)
                self.assertTrue(all(bill in cajero.billetes for bill in bills))

    def test_non_integer_amounts_are_rejected_without_raising(self):
        for amount in (100.0, True, "100", None):
            with self.subTest(amount=amount):
                cajero = Cajero()

                message, authorized = cajero.mensaje_retiro(amount)

                self.assertFalse(authorized)
                self.assertEqual(message, "Monto inválido")
                self.assertEqual(cajero.entregar_dinero(amount), [])
                self.assertEqual(cajero.dinero, 50_000)

    def test_balance_update_cannot_create_an_invalid_balance(self):
        cajero = Cajero()

        for amount in (-100, 50_001, 100.0, True):
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    cajero.actualizar_dinero(amount)
                self.assertEqual(cajero.dinero, 50_000)


if __name__ == "__main__":
    unittest.main()
