import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import flet as ft

from main import App, Listing, main, read_listing, status_text
from shell import Shell
from ui import EntryRow

from .render import render


class ListingTests(unittest.TestCase):
    def test_read_listing_applies_the_search_only_to_the_current_folder(self):
        with TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "a.txt").write_text("x")
            (base / "sub").mkdir()
            (base / "sub" / "a-dentro.txt").write_text("x")

            listing = read_listing(Shell(base), "a")

            self.assertEqual([p.name for p in listing.entries], ["a.txt"])
            self.assertEqual(listing.total, 2)

    def test_status_text(self):
        entries = [Path("a")]
        self.assertEqual(status_text(Listing(entries, 1), ""), "1 elemento")
        self.assertEqual(status_text(Listing(entries * 2, 2), ""), "2 elementos")
        self.assertEqual(
            status_text(Listing(entries, 4), " a "), "1 de 4 elementos coinciden con «a»"
        )
        self.assertEqual(status_text(Listing([], 0, "boom"), ""), "Error al cargar el contenido.")


class AppRenderTests(unittest.TestCase):
    def test_app_lists_the_entries_of_the_start_folder(self):
        with TemporaryDirectory() as tmp:
            (Path(tmp) / "uno.txt").write_text("x")
            (Path(tmp) / "carpeta").mkdir()

            with patch("main.Shell", lambda: Shell(tmp)):
                controls = render(App)

            names = [c.value for c in controls if isinstance(c, ft.Text)]
            self.assertIn("uno.txt", names)
            self.assertIn("carpeta", names)
            self.assertTrue(any(isinstance(c, ft.TextField) for c in controls))

    def test_empty_folder_shows_a_message(self):
        with TemporaryDirectory() as tmp, patch("main.Shell", lambda: Shell(tmp)):
            controls = render(App)

        self.assertIn("Esta carpeta está vacía.", [c.value for c in controls if isinstance(c, ft.Text)])

    def test_entry_row_disables_opening_for_files(self):
        with TemporaryDirectory() as tmp:
            file = Path(tmp) / "a.txt"
            file.write_text("x")
            controls = render(EntryRow, file, on_open=print, on_rename=print, on_delete=print)

        opener = [c for c in controls if isinstance(c, ft.IconButton)][-1]
        self.assertTrue(opener.disabled)

    def test_main_is_callable(self):
        self.assertTrue(callable(main))


if __name__ == "__main__":
    unittest.main()
