"""Verifica que la interfaz pueda importarse sin iniciar Flet."""

import unittest


class CajeroAppTests(unittest.TestCase):
    def test_app_is_importable_as_a_package_module(self) -> None:
        from cajero.app import main

        self.assertTrue(callable(main))


if __name__ == "__main__":
    unittest.main()
