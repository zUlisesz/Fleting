import unittest

import flet as ft

from components.atoms import Button, IconButton, SearchInput, Surface, TextInput
from components.atoms.button import VARIANTS, button_style

from .render import render


class ButtonTests(unittest.TestCase):
    def test_default_is_filled_and_outline_is_outlined(self) -> None:
        self.assertIsInstance(render(Button, "Ok")[0], ft.FilledButton)
        self.assertIsInstance(render(Button, "Ok", variant="outline")[0], ft.OutlinedButton)

    def test_unknown_variant_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            button_style("ghost")  # type: ignore[arg-type]

    def test_every_variant_has_a_style(self) -> None:
        for variant in VARIANTS:
            with self.subTest(variant=variant):
                self.assertIsInstance(button_style(variant), ft.ButtonStyle)

    def test_disabled_flag_is_forwarded(self) -> None:
        self.assertTrue(render(Button, "Ok", disabled=True)[0].disabled)


class InputTests(unittest.TestCase):
    def test_text_input_is_controlled_by_value(self) -> None:
        field = render(TextInput, "Nombre", value="Ada")[0]

        self.assertIsInstance(field, ft.TextField)
        self.assertEqual(field.value, "Ada")

    def test_search_input_has_a_search_icon(self) -> None:
        field = render(SearchInput, hint_text="Buscar")[0]

        self.assertEqual(field.prefix_icon, ft.Icons.SEARCH)
        self.assertEqual(field.hint_text, "Buscar")


class MiscAtomTests(unittest.TestCase):
    def test_icon_button_uses_the_given_size(self) -> None:
        button = render(IconButton, ft.Icons.HOME, size=50)[0]

        self.assertEqual((button.width, button.height), (50, 50))

    def test_surface_wraps_its_content(self) -> None:
        text = ft.Text("hola")
        controls = render(Surface, text)

        self.assertIsInstance(controls[0], ft.Container)
        self.assertIn(text, controls)


if __name__ == "__main__":
    unittest.main()
