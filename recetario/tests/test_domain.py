import unittest

from domain import IngredientLine, Instruction, RecipeDetail


def line(amount=None, unit=None) -> IngredientLine:
    return IngredientLine(link_id="l", ingredient_id="i", name="Sal", unit=unit, amount=amount)


class IngredientLineTests(unittest.TestCase):
    def test_quantity_combines_amount_and_unit(self):
        self.assertEqual(line("2", "piezas").quantity, "2 piezas")
        self.assertEqual(line("2").quantity, "2")
        self.assertEqual(line(unit="g").quantity, "g")
        self.assertEqual(line().quantity, "")


class RecipeDetailTests(unittest.TestCase):
    def step(self, number: int) -> Instruction:
        return Instruction(id=f"s{number}", recipe_id="r", step_number=number, instruction="x")

    def test_next_step_number_follows_the_highest_step(self):
        self.assertEqual(RecipeDetail(id="r", title="Sopa").next_step_number, 1)
        detail = RecipeDetail(id="r", title="Sopa", instructions=[self.step(1), self.step(4)])
        self.assertEqual(detail.next_step_number, 5)


if __name__ == "__main__":
    unittest.main()
