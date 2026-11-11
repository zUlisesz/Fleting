"""Verifica que la vista de Cards pueda importarse sin iniciar Flet."""

import unittest


class CardsMainTests(unittest.TestCase):
    def test_main_is_importable_as_a_package_module(self) -> None:
        from cards.main import main

        self.assertTrue(callable(main))


if __name__ == "__main__":
    unittest.main()
