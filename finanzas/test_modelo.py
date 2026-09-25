import sqlite3
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from .modelo import Repositorio, moneda_firmada, resumir


class RepositorioTest(unittest.TestCase):
    def crear_repositorio(self):
        directorio = TemporaryDirectory()
        self.addCleanup(directorio.cleanup)
        return Repositorio(Path(directorio.name) / "finanzas.sqlite3")

    def test_resume_ingresos_gastos_y_saldo(self):
        repo = self.crear_repositorio()
        repo.agregar("2026-09-01", "Sueldo", "Trabajo", "Ingreso", "1000.00")
        repo.agregar("2026-09-02", "Comida", "Comida", "Gasto", "125.50")

        resumen = resumir(repo.listar())

        self.assertEqual(resumen["ingresos"], 100000)
        self.assertEqual(resumen["gastos"], 12550)
        self.assertEqual(resumen["balance"], 87450)
        self.assertEqual(moneda_firmada(-12550), "-$125.50")
        self.assertEqual(repo.ingresos(), 100000)
        self.assertEqual(repo.gastos(), 12550)

    def test_filtra_por_tipo_y_elimina_movimiento(self):
        repo = self.crear_repositorio()
        ingreso = repo.agregar("2026-09-01", "Sueldo", "Trabajo", "Ingreso", "100.00")
        repo.agregar("2026-09-02", "Comida", "Comida", "Gasto", "20.00")

        ingresos = repo.listar(tipo="Ingreso")

        self.assertEqual([movimiento.id for movimiento in ingresos], [ingreso])
        repo.eliminar(ingreso)
        movimientos = repo.listar()
        self.assertEqual(len(movimientos), 1)
        self.assertEqual(movimientos[0].tipo, "Gasto")
        self.assertEqual(repo.ingresos(), 0)

    def test_migra_la_tabla_gastos_existente(self):
        with TemporaryDirectory() as directorio:
            ruta = Path(directorio) / "finanzas.sqlite3"
            with sqlite3.connect(ruta) as con:
                con.execute("""CREATE TABLE gastos (
                    id INTEGER PRIMARY KEY, fecha TEXT NOT NULL, concepto TEXT NOT NULL,
                    categoria TEXT NOT NULL, centavos INTEGER NOT NULL)""")
                con.execute(
                    "INSERT INTO gastos VALUES (7, '2026-08-01', 'Ahorro anterior', 'Ahorro', 5000)"
                )

            movimientos = Repositorio(ruta).listar()

        self.assertEqual(len(movimientos), 1)
        self.assertEqual(movimientos[0].tipo, "Gasto")
        self.assertEqual(movimientos[0].centavos, 5000)


if __name__ == "__main__":
    unittest.main()
