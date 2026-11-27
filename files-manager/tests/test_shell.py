from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from shell import Shell, describe, match_name


class ShellTests(unittest.TestCase):
    def test_rejects_an_invalid_initial_directory_value(self):
        for start_path in (0, True):
            with self.subTest(start_path=start_path):
                with self.assertRaises(ValueError):
                    Shell(start_path)

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

    def test_rejects_a_non_text_route_before_navigating(self):
        with TemporaryDirectory() as temporary_directory:
            shell = Shell(temporary_directory)

            with self.assertRaises(ValueError):
                shell.cd(None)

            self.assertEqual(shell.cwd, Path(temporary_directory).resolve())


class SearchTests(unittest.TestCase):
    """La búsqueda solo ve los elementos directos de la carpeta actual."""

    def setUp(self):
        self._tmp = TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name).resolve()
        (self.base / "inicio").mkdir()
        (self.base / "inicio" / "nota.txt").write_text("a")
        (self.base / "inicio" / "Informe.pdf").write_text("b")
        (self.base / "inicio" / "sub").mkdir()
        (self.base / "inicio" / "sub" / "nota-interna.txt").write_text("c")
        (self.base / "hermana").mkdir()
        (self.base / "hermana" / "nota-hermana.txt").write_text("d")
        (self.base / "nota-raiz.txt").write_text("e")
        self.shell = Shell(self.base)
        self.shell.cd("inicio")

    def names(self, query):
        return [p.name for p in self.shell.search(query)]

    def test_finds_files_in_the_current_directory(self):
        self.assertEqual(self.names("nota"), ["nota.txt"])

    def test_is_case_insensitive(self):
        self.assertEqual(self.names("INFORME"), ["Informe.pdf"])

    def test_does_not_find_files_inside_subdirectories(self):
        self.assertNotIn("nota-interna.txt", self.names("nota"))
        self.assertEqual(self.names("interna"), [])

    def test_does_not_find_files_outside_the_current_directory(self):
        self.assertEqual(self.names("raiz"), [])
        self.assertEqual(self.names("hermana"), [])

    def test_finds_a_subdirectory_by_its_own_name(self):
        self.assertEqual(self.names("sub"), ["sub"])

    def test_scope_follows_the_current_directory(self):
        self.shell.cd("sub")

        self.assertEqual(self.names("nota"), ["nota-interna.txt"])
        self.shell.cd("..")
        self.shell.cd("..")
        self.assertEqual(self.names("nota"), ["nota-raiz.txt"])

    def test_blank_query_returns_everything(self):
        self.assertEqual(self.shell.search("  "), self.shell.ls())

    def test_rejects_a_non_text_query(self):
        with self.assertRaises(ValueError):
            self.shell.search(None)

    def test_hidden_entries_are_never_listed(self):
        (self.base / "inicio" / ".nota-oculta").write_text("x")

        self.assertEqual(self.names("nota"), ["nota.txt"])


class HelperTests(unittest.TestCase):
    def test_match_name_filters_by_substring(self):
        entries = [Path("a/Foto.png"), Path("a/texto.txt")]

        self.assertEqual(match_name(entries, "FOTO"), [entries[0]])

    def test_describe_formats_files_and_folders(self):
        with TemporaryDirectory() as tmp:
            file = Path(tmp) / "a.txt"
            file.write_text("hola")

            self.assertEqual(describe(file), "4 bytes")
            self.assertEqual(describe(Path(tmp)), "Carpeta")
            self.assertEqual(describe(Path(tmp) / "no-existe"), "No disponible")


if __name__ == "__main__":
    unittest.main()
