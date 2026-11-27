import unittest

from finanzas.dominio import (
    Filtros,
    Movimiento,
    a_centavos,
    moneda,
    moneda_firmada,
    resumir,
    validar_fecha,
    validar_texto,
)


class ImporteTests(unittest.TestCase):
    def test_converts_valid_amounts_to_cents(self):
        for texto, centavos in (("120.50", 12050), ("120,5", 12050), ("1", 100), (" 0.01 ", 1)):
            with self.subTest(texto=texto):
                self.assertEqual(a_centavos(texto), centavos)

    def test_rejects_invalid_amounts(self):
        for texto in ("1.005", "NaN", "0", "-5", "1,000.00", "", "10000000", "abc"):
            with self.subTest(texto=texto):
                with self.assertRaises(ValueError):
                    a_centavos(texto)

    def test_rejects_non_text_amounts(self):
        for valor in (None, 20, True):
            with self.subTest(valor=valor):
                with self.assertRaises(ValueError):
                    a_centavos(valor)

    def test_formats_currency(self):
        self.assertEqual(moneda(123456), "$1,234.56")
        self.assertEqual(moneda_firmada(-5), "-$0.05")
        self.assertEqual(moneda_firmada(5), "$0.05")


class ValidacionTests(unittest.TestCase):
    def test_dates_must_be_real_and_iso(self):
        self.assertEqual(validar_fecha("2026-11-10"), "2026-11-10")
        for fecha in ("2026-13-01", "10/11/2026", "2026-1-5", None):
            with self.subTest(fecha=fecha):
                with self.assertRaises(ValueError):
                    validar_fecha(fecha)

    def test_text_is_trimmed_and_bounded(self):
        self.assertEqual(validar_texto("  Ana ", "nombre"), "Ana")
        for valor in ("", "   ", "x" * 81, None, 5):
            with self.subTest(valor=valor):
                with self.assertRaises(ValueError):
                    validar_texto(valor, "nombre")

    def test_filters_are_validated(self):
        self.assertEqual(Filtros("Comida", "2026-09", "Gasto").validar().mes, "2026-09")
        for filtros in (Filtros(categoria="X"), Filtros(tipo="X"), Filtros(mes="2026-13"), Filtros(mes="26-1")):
            with self.subTest(filtros=filtros):
                with self.assertRaises(ValueError):
                    filtros.validar()


class ResumenTests(unittest.TestCase):
    def test_summary_totals_and_balance(self):
        movimientos = [
            Movimiento(1, "2026-11-01", "Nómina", "Trabajo", "Ingreso", 100_000),
            Movimiento(2, "2026-11-02", "Comida", "Comida", "Gasto", 12_550),
        ]

        resumen = resumir(movimientos)

        self.assertEqual((resumen.ingresos, resumen.gastos), (100_000, 12_550))
        self.assertEqual(resumen.balance, 87_450)
        self.assertEqual(resumen.cantidad, 2)
        self.assertEqual(resumen.categorias["Gasto · Comida"], 12_550)

    def test_empty_summary_is_zero(self):
        resumen = resumir([])

        self.assertEqual((resumen.total, resumen.balance, resumen.cantidad), (0, 0, 0))


if __name__ == "__main__":
    unittest.main()
