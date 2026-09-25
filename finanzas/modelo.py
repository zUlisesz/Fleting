"""Importes en centavos enteros y consultas SQLite parametrizadas."""
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
import re
import sqlite3

CATEGORIAS = ("Comida", "Transporte", "Estudio", "Hogar", "Ocio", "Ahorro", "Trabajo", "Otros")
TIPOS = ("Gasto", "Ingreso")


def a_centavos(texto: str) -> int:
    limpio = texto.strip()
    if not re.fullmatch(r"\d+(?:[.,]\d{1,2})?", limpio):
        raise ValueError("Usa un importe positivo con hasta dos decimales, sin separador de miles.")
    try:
        valor = Decimal(limpio.replace(",", "."))
    except InvalidOperation as error:
        raise ValueError("Importe inválido.") from error
    if not Decimal("0") < valor <= Decimal("9999999.99"):
        raise ValueError("El importe debe ser mayor que cero y no superar 9,999,999.99.")
    return int(valor * 100)


def moneda(centavos: int) -> str:
    return f"${centavos // 100:,}.{centavos % 100:02d}"


@dataclass(frozen=True)
class Movimiento:
    id: int
    fecha: str
    concepto: str
    categoria: str
    tipo: str
    centavos: int

def resumir(gastos: list[Movimiento]) -> dict:
    categorias = {}
    for gasto in gastos:
        categorias[gasto.categoria] = categorias.get(gasto.categoria, 0) + gasto.centavos
    return {"total": sum(g.centavos for g in gastos), "cantidad": len(gastos), "categorias": categorias}


class Repositorio:
    def __init__(self, ruta: Path):
        self.ruta = Path(ruta)
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        with self.conexion() as con:
            con.execute("""CREATE TABLE IF NOT EXISTS movimientos (
                id INTEGER PRIMARY KEY, fecha TEXT NOT NULL, concepto TEXT NOT NULL,
                categoria TEXT NOT NULL, tipo TEXT NOT NULL, centavos INTEGER NOT NULL CHECK(centavos > 0))""")

    @contextmanager
    def conexion(self):
        con = sqlite3.connect(self.ruta, timeout=10)
        try:
            with con:
                yield con
        finally:
            con.close()

    def agregar(self, fecha: str, concepto: str, categoria: str, tipo: str,  importe: str):
        try:
            fecha_normal = date.fromisoformat(fecha).isoformat()
        except (ValueError, TypeError) as error:
            raise ValueError("Introduce una fecha real en formato AAAA-MM-DD.") from error
        if fecha_normal != fecha:
            raise ValueError("Usa formato AAAA-MM-DD.")
        concepto = concepto.strip()
        if not 1 <= len(concepto) <= 80:
            raise ValueError("El concepto debe tener entre 1 y 80 caracteres.")
        if categoria not in CATEGORIAS:
            raise ValueError("Selecciona una categoría válida.")
        if tipo not in TIPOS:
            raise ValueError("Selecciona un tipo de movimiento válido.")
        centavos = a_centavos(importe)
        with self.conexion() as con:
            return con.execute("INSERT INTO movimientos(fecha,concepto,categoria,tipo,centavos) VALUES (?,?,?,?,?)", (fecha, concepto, categoria,tipo ,centavos)).lastrowid

    def listar(self, categoria="Todas", mes="") -> list[Movimiento]:
        if categoria != "Todas" and categoria not in CATEGORIAS:
            raise ValueError("Categoría de filtro inválida.")
        if mes:
            if not re.fullmatch(r"\d{4}-\d{2}", mes):
                raise ValueError("El mes debe tener formato AAAA-MM.")
            try:
                date.fromisoformat(mes + "-01")
            except ValueError as error:
                raise ValueError("Mes inválido.") from error
        consulta = "SELECT id,fecha,concepto,categoria, tipo, centavos FROM movimientos WHERE 1=1"
        parametros = []
        if categoria != "Todas":
            consulta += " AND categoria=?"
            parametros.append(categoria)
        if mes:
            consulta += " AND substr(fecha,1,7)=?"
            parametros.append(mes)
        with self.conexion() as con:
            return [Movimiento(*fila) for fila in con.execute(consulta + " ORDER BY fecha DESC, id DESC", parametros)]

    def gastos(self):
        key = 'Gasto'
        with self.conexion() as con:
            cursor = con.execute("SELECT centavos FROM movimientos WHERE tipo = ?", (key,))
            return sum ( [ element[0] for element in cursor.fetchall()] ) 

    def ingresos(self):
        key = 'Ingreso'
        with self.conexion() as con:
            cursor = con.execute("SELECT centavos FROM movimientos WHERE tipo = ?", (key,))
            return sum ( [ element[0] for element in cursor.fetchall()] ) 

    def eliminar(self, id: int):
        with self.conexion() as con:
            cursor = con.execute("DELETE FROM gastos WHERE id=?", (id,))
            if cursor.rowcount != 1:
                raise ValueError("El movimiento ya no existe.")
