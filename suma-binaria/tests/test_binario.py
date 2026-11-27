import unittest

from binario import MAX_BITS, Suma, es_binario, sumar


class EsBinarioTests(unittest.TestCase):
    def test_accepts_only_zeros_and_ones(self):
        for value in ("0", "1", "0101", "0010"):
            with self.subTest(value=value):
                self.assertTrue(es_binario(value))

    def test_rejects_empty_non_binary_and_non_text_values(self):
        for value in ("", "102", "abc", " 1", "1 ", "-1", None, 10, True):
            with self.subTest(value=value):
                self.assertFalse(es_binario(value))


class SumarTests(unittest.TestCase):
    def test_adds_valid_binary_numbers(self):
        self.assertEqual(sumar("101", "11").resultado.lstrip("0"), "1000")
        self.assertEqual(sumar("0", "0").decimal, (0, 0, 0))

    def test_exposes_the_decimal_equivalent(self):
        self.assertEqual(sumar("101", "11").decimal, (5, 3, 8))

    def test_carries_enter_each_column_from_the_right(self):
        suma = sumar("101", "11")  # 0101 + 0011 = 1000

        self.assertEqual(suma.ancho, 4)
        self.assertEqual(suma.acarreos, "1110")
        self.assertEqual(suma.resultado, "1000")

    def test_the_result_gains_a_bit_on_overflow(self):
        suma = sumar("11", "1")

        self.assertEqual(suma.resultado, "100")
        self.assertEqual(suma.ancho, 3)
        self.assertEqual(suma.decimal[2], 4)

    def test_operands_keep_what_the_user_typed(self):
        suma = sumar("0010", "1")

        self.assertEqual((suma.primero, suma.segundo), ("0010", "1"))
        self.assertEqual(suma.decimal, (2, 1, 3))

    def test_matches_integer_addition_for_every_pair_up_to_five_bits(self):
        for a in range(32):
            for b in range(32):
                with self.subTest(a=a, b=b):
                    suma = sumar(format(a, "b"), format(b, "b"))
                    self.assertEqual(suma.decimal, (a, b, a + b))

    def test_rejects_invalid_input_with_a_message(self):
        for first, second in (("", "1"), ("1", ""), ("102", "1"), ("1", "abc"), (None, "1"), (10, "1")):
            with self.subTest(first=first, second=second):
                with self.assertRaisesRegex(ValueError, "ceros y unos"):
                    sumar(first, second)

    def test_rejects_numbers_over_the_bit_limit(self):
        self.assertTrue(sumar("1" * MAX_BITS, "1").resultado)
        with self.assertRaisesRegex(ValueError, str(MAX_BITS)):
            sumar("1" * (MAX_BITS + 1), "1")

    def test_result_is_immutable(self):
        with self.assertRaises(AttributeError):
            sumar("1", "1").resultado = "0"  # type: ignore[misc]
        self.assertIsInstance(sumar("1", "1"), Suma)


if __name__ == "__main__":
    unittest.main()
