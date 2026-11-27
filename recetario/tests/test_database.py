"""Consultas y repositorios con una conexión simulada (no hace falta MySQL)."""

import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

import mysql.connector

from database import StorageError, execute, fetch_all, fetch_one
from domain import Ingredient, Instruction, Recipe, RecipeIngredient
from repositories import (
    IngredientRepository,
    InstructionRepository,
    RecipeIngredientRepository,
    RecipeRepository,
)


def fake_connection(cursor: MagicMock) -> MagicMock:
    """Conexión que sirve como context manager y entrega ``cursor``."""
    connection = MagicMock()
    connection.__enter__.return_value = connection
    connection.cursor.return_value.__enter__.return_value = cursor
    return connection


class QueryTests(unittest.TestCase):
    def run_with(self, cursor: MagicMock):
        connection = fake_connection(cursor)
        patcher = patch("database.query.get_connection", return_value=connection)
        patcher.start()
        self.addCleanup(patcher.stop)
        return connection

    def test_fetch_all_and_fetch_one_use_a_dictionary_cursor_and_do_not_commit(self):
        cursor = MagicMock()
        cursor.fetchall.return_value = [{"id": "1"}]
        cursor.fetchone.return_value = {"id": "1"}
        connection = self.run_with(cursor)

        self.assertEqual(fetch_all("SELECT 1 WHERE a = %s", ("x",)), [{"id": "1"}])
        self.assertEqual(fetch_one("SELECT 1"), {"id": "1"})

        connection.cursor.assert_called_with(dictionary=True)
        cursor.execute.assert_any_call("SELECT 1 WHERE a = %s", ("x",))
        connection.commit.assert_not_called()

    def test_execute_commits_and_returns_the_affected_rows(self):
        cursor = MagicMock(rowcount=3)
        connection = self.run_with(cursor)

        self.assertEqual(execute("DELETE FROM t WHERE a = %s", ["x"]), 3)

        cursor.execute.assert_called_once_with("DELETE FROM t WHERE a = %s", ("x",))
        connection.commit.assert_called_once_with()

    def test_driver_errors_become_storage_errors_and_nothing_is_committed(self):
        cursor = MagicMock()
        cursor.execute.side_effect = mysql.connector.Error("boom")
        connection = self.run_with(cursor)

        with self.assertRaisesRegex(StorageError, "boom"):
            execute("DELETE FROM t")
        connection.commit.assert_not_called()

    def test_connection_failures_become_storage_errors(self):
        with patch("database.query.get_connection", side_effect=mysql.connector.Error("sin servidor")):
            with self.assertRaisesRegex(StorageError, "sin servidor"):
                fetch_all("SELECT 1")


class RepositoryTests(unittest.TestCase):
    def test_recipe_repository_maps_rows_to_models(self):
        created = datetime(2026, 1, 1)
        with patch("repositories.recipe.fetch_all", return_value=[{"id": "1", "title": "A", "created_at": created}]):
            self.assertEqual(RecipeRepository().list_all(), [Recipe(id="1", title="A", created_at=created)])
        with patch("repositories.recipe.fetch_one", return_value=None):
            self.assertIsNone(RecipeRepository().get("x"))

    def test_mutations_report_whether_a_row_changed(self):
        with patch("repositories.recipe.execute", return_value=0) as run:
            self.assertFalse(RecipeRepository().delete("x"))
        run.assert_called_once_with("DELETE FROM recipes WHERE id = %s", ("x",))
        with patch("repositories.recipe.execute", return_value=1):
            self.assertTrue(RecipeRepository().update_title("x", "T"))

    def test_create_methods_pass_the_model_fields_in_order(self):
        with patch("repositories.recipe.execute") as run:
            RecipeRepository().create(Recipe(id="r", title="T"))
        self.assertEqual(run.call_args.args[1], ("r", "T"))

        with patch("repositories.ingredient.execute") as run:
            IngredientRepository().create(Ingredient(id="i", name="Sal", unit="g"))
        self.assertEqual(run.call_args.args[1], ("i", "Sal", "g"))

        with patch("repositories.instruction.execute") as run:
            InstructionRepository().create(Instruction(id="s", recipe_id="r", step_number=2, instruction="x"))
        self.assertEqual(run.call_args.args[1], ("s", "r", 2, "x"))

        with patch("repositories.recipe_ingredient.execute") as run:
            RecipeIngredientRepository().add(RecipeIngredient(id="l", recipe_id="r", ingredient_id="i", amount="1"))
        self.assertEqual(run.call_args.args[1], ("l", "r", "i", "1"))

    def test_ingredient_lookup_and_listing_map_rows(self):
        with patch("repositories.ingredient.fetch_one", return_value={"id": "i", "name": "Sal", "unit": None}):
            self.assertEqual(IngredientRepository().get_by_name("sal"), Ingredient(id="i", name="Sal"))

        row = {"link_id": "l", "ingredient_id": "i", "amount": "2", "name": "Sal", "unit": "g"}
        with patch("repositories.recipe_ingredient.fetch_all", return_value=[row]) as run:
            lines = RecipeIngredientRepository().list_for_recipe("r")
        self.assertEqual(lines[0].quantity, "2 g")
        self.assertEqual(run.call_args.args[1], ("r",))


if __name__ == "__main__":
    unittest.main()
