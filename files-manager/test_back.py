from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from back import Shell


class ShellTests(unittest.TestCase):
    def test_cannot_navigate_above_the_initial_directory(self):
        with TemporaryDirectory() as temporary_directory:
            shell = Shell(temporary_directory)

            self.assertFalse(shell.can_go_up())

            with self.assertRaises(ValueError):
                shell.cd("..")

            self.assertEqual(shell.cwd, Path(temporary_directory).resolve())

    def test_can_navigate_inside_the_initial_directory(self):
        with TemporaryDirectory() as temporary_directory:
            child = Path(temporary_directory) / "documentos"
            child.mkdir()
            shell = Shell(temporary_directory)

            shell.cd("documentos")

            self.assertEqual(shell.cwd, child.resolve())
            self.assertEqual(shell.relative_pwd(), "documentos")
            self.assertTrue(shell.can_go_up())


if __name__ == "__main__":
    unittest.main()
