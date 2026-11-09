"""Pruebas de importación para que el catálogo pueda ejecutarse como paquete."""

from pathlib import Path
import subprocess
import sys
import unittest


class PackageImportTests(unittest.TestCase):
    def test_main_and_public_atoms_are_importable(self) -> None:
        """Los imports relativos permiten usar ``python -m components.main``."""
        import components.main  # noqa: F401
        from components.atoms import search_input, shadcn_button, surface

        self.assertTrue(callable(search_input))
        self.assertTrue(callable(shadcn_button))
        self.assertTrue(callable(surface))

    def test_main_is_importable_from_its_own_directory(self) -> None:
        """La ejecución directa conserva los imports compatibles previos."""
        result = subprocess.run(
            [sys.executable, "-c", "import main"],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
