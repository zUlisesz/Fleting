import unittest

import flet as ft

from components.app import App
from components.gallery import SECTIONS
from components.gallery._catalog import filter_members, page_count, page_slice
from components.gallery.gradients import GRADIENTS, GROUPS, filter_gradients
from components.gallery.styled_buttons import STYLES, spec_style

from .render import render


class SectionTests(unittest.TestCase):
    def test_section_keys_are_unique(self) -> None:
        keys = [s.key for s in SECTIONS]

        self.assertEqual(len(keys), len(set(keys)))

    def test_every_gallery_renders_without_errors(self) -> None:
        for section in SECTIONS:
            with self.subTest(section=section.key):
                self.assertGreater(len(render(section.view, key=section.key)), 1)

    def test_app_renders_with_the_navigation_rail(self) -> None:
        controls = render(App)

        self.assertTrue(any(isinstance(c, ft.NavigationRail) for c in controls))


class CatalogTests(unittest.TestCase):
    def test_filter_is_case_insensitive_and_trims(self) -> None:
        matches = filter_members(tuple(ft.Colors), "  BLUE ")

        self.assertTrue(matches)
        self.assertTrue(all("blue" in c.name.lower() for c in matches))

    def test_empty_query_keeps_every_member(self) -> None:
        self.assertEqual(len(filter_members(tuple(ft.Colors), "")), len(ft.Colors))

    def test_page_count_is_at_least_one(self) -> None:
        self.assertEqual(page_count(0), 1)
        self.assertEqual(page_count(120), 1)
        self.assertEqual(page_count(121), 2)

    def test_page_slice_returns_the_requested_window(self) -> None:
        self.assertEqual(list(page_slice(range(10), 1, 4)), [4, 5, 6, 7])
        self.assertEqual(list(page_slice(range(10), 2, 4)), [8, 9])


class DataTests(unittest.TestCase):
    def test_gradient_names_are_unique_and_grouped(self) -> None:
        names = [g.name for g in GRADIENTS]

        self.assertEqual(len(names), len(set(names)))
        self.assertTrue({g.group for g in GRADIENTS} <= set(GROUPS))

    def test_group_filter(self) -> None:
        self.assertEqual(filter_gradients("Todos"), GRADIENTS)
        self.assertTrue(all(g.group == "Sweep" for g in filter_gradients("Sweep")))

    def test_button_styles_have_unique_titles_and_valid_styles(self) -> None:
        titles = [title for title, _ in STYLES]

        self.assertEqual(len(titles), len(set(titles)))
        for _, spec in STYLES:
            self.assertIsInstance(spec_style(spec), ft.ButtonStyle)


if __name__ == "__main__":
    unittest.main()
