import subprocess
import sys
import unittest
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parents[1]


class ImportTests(unittest.TestCase):
    def test_package_entry_point_is_importable(self) -> None:
        from components.main import main

        self.assertTrue(callable(main))

    def test_main_can_be_imported_from_its_own_directory(self) -> None:
        """``flet run main.py`` ejecuta el archivo como script."""
        result = subprocess.run(
            [sys.executable, "-c", "import main"],
            cwd=PACKAGE_DIR,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
