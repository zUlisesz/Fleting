"""Pruebas de importación para que el catálogo pueda ejecutarse como paquete."""

import unittest


class PackageImportTests(unittest.TestCase):
    def test_main_and_public_atoms_are_importable(self) -> None:
        """Los imports relativos permiten usar ``python -m components.main``."""
        import components.main  # noqa: F401
        from components.atoms import search_input, shadcn_button, surface

        self.assertTrue(callable(search_input))
        self.assertTrue(callable(shadcn_button))
        self.assertTrue(callable(surface))


if __name__ == "__main__":
    unittest.main()
