"""Verifica la interfaz sin abrir una ventana de Flet."""

import unittest
from types import SimpleNamespace

import flet as ft


class CajeroAppTests(unittest.TestCase):
    def setUp(self) -> None:
        from cajero.main import CajeroView

        self.page = SimpleNamespace(services=[])
        self.view = CajeroView(self.page)
        self.view.build()

    def test_app_is_importable_as_a_package_module(self) -> None:
        from cajero.main import main

        self.assertTrue(callable(main))

    def test_audio_services_are_registered_on_the_page(self) -> None:
        self.assertEqual(len(self.page.services), 2)

    def test_build_returns_a_row(self) -> None:
        self.assertIsInstance(self.view.build(), ft.Row)

    def test_valid_withdrawal_shows_bills(self) -> None:
        self.view.monto.value = "1700"

        self.assertTrue(self.view.retirar())
        self.assertEqual(len(self.view.billetes.controls), 3)
        self.assertEqual(self.view.cajero.dinero, 48_300)

    def test_empty_or_invalid_withdrawal_clears_bills(self) -> None:
        for texto in ("", "150", "9000"):
            with self.subTest(texto=texto):
                self.view.monto.value = texto

                self.assertFalse(self.view.retirar())
                self.assertEqual(self.view.billetes.controls, [])
                self.assertEqual(self.view.cajero.dinero, 50_000)


if __name__ == "__main__":
    unittest.main()
