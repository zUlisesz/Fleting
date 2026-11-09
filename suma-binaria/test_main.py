"""Pruebas de la lógica de suma binaria sin abrir la interfaz Flet."""

import importlib.util
from pathlib import Path
import unittest


def _load_module():
    module_path = Path(__file__).with_name("main.py")
    spec = importlib.util.spec_from_file_location("suma_binaria_main", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class BinaryAdditionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = _load_module()

    def test_adds_valid_binary_numbers(self) -> None:
        self.assertEqual(self.module.suma("101", "11"), "1000")
        self.assertEqual(self.module.suma("0", "0"), "0")

    def test_rejects_empty_or_non_binary_values(self) -> None:
        for value in ("", "102", "abc"):
            with self.subTest(value=value):
                self.assertFalse(self.module.bin_valid(value))
                self.assertEqual(
                    self.module.suma(value, "1"),
                    "TYPE VALID BINARY NUMBERS",
                )


if __name__ == "__main__":
    unittest.main()
