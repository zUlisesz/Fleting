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

    def test_renames_a_direct_child_without_leaving_the_initial_directory(self):
        with TemporaryDirectory() as temporary_directory:
            original = Path(temporary_directory) / "nota.txt"
            original.write_text("contenido")
            shell = Shell(temporary_directory)

            renamed = shell.rename("nota.txt", "tarea.txt")

            self.assertEqual(renamed.name, "tarea.txt")
            self.assertTrue(renamed.is_file())
            self.assertFalse(original.exists())
            with self.assertRaises(ValueError):
                shell.rename("tarea.txt", "../fuera.txt")

    def test_rejects_non_text_names_before_accessing_the_filesystem(self):
        with TemporaryDirectory() as temporary_directory:
            shell = Shell(temporary_directory)

            for operation, arguments in (
                (shell.mkdir, (None,)),
                (shell.rm, (None,)),
                (shell.rename, (None, "archivo.txt")),
            ):
                with self.subTest(operation=operation.__name__):
                    with self.assertRaises(ValueError):
                        operation(*arguments)


if __name__ == "__main__":
    unittest.main()
