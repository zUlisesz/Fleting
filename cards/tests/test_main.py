"""Verifica la vista de Cards sin iniciar Flet."""

import unittest

class CardsMainTests(unittest.TestCase):
    def test_main_and_components_are_importable(self) -> None:
        from cards.main import App, Toolbar, UserCard, main

        for obj in (main, App, Toolbar, UserCard):
            self.assertTrue(callable(obj))


if __name__ == "__main__":
    unittest.main()
