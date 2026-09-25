"""Importes en centavos enteros y consultas SQLite parametrizadas."""
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
import re
import sqlite3

CATEGORIAS = ("Comida", "Transporte", "Estudio", "Hogar", "Ocio", "Otros")


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
class Gasto:
    id: int
    fecha: str
    concepto: str
    categoria: str
    centavos: int


def resumir(gastos: list[Gasto]) -> dict:
    categorias = {}
    for gasto in gastos:
        categorias[gasto.categoria] = categorias.get(gasto.categoria, 0) + gasto.centavos
    return {"total": sum(g.centavos for g in gastos), "cantidad": len(gastos), "categorias": categorias}


class Repositorio:
    def __init__(self, ruta: Path):
        self.ruta = Path(ruta)
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        with self.conexion() as con:
            con.execute("""CREATE TABLE IF NOT EXISTS gastos (
                id INTEGER PRIMARY KEY, fecha TEXT NOT NULL, concepto TEXT NOT NULL,
                categoria TEXT NOT NULL, centavos INTEGER NOT NULL CHECK(centavos > 0))""")

    @contextmanager
    def conexion(self):
        con = sqlite3.connect(self.ruta, timeout=10)
        try:
            with con:
                yield con
        finally:
            con.close()

    def agregar(self, fecha: str, concepto: str, categoria: str, importe: str):
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
        centavos = a_centavos(importe)
        with self.conexion() as con:
            return con.execute("INSERT INTO gastos(fecha,concepto,categoria,centavos) VALUES (?,?,?,?)", (fecha, concepto, categoria, centavos)).lastrowid

    def listar(self, categoria="Todas", mes="") -> list[Gasto]:
        if categoria != "Todas" and categoria not in CATEGORIAS:
            raise ValueError("Categoría de filtro inválida.")
        if mes:
            if not re.fullmatch(r"\d{4}-\d{2}", mes):
                raise ValueError("El mes debe tener formato AAAA-MM.")
            try:
                date.fromisoformat(mes + "-01")
            except ValueError as error:
                raise ValueError("Mes inválido.") from error
        consulta = "SELECT id,fecha,concepto,categoria,centavos FROM gastos WHERE 1=1"
        parametros = []
        if categoria != "Todas":
            consulta += " AND categoria=?"
            parametros.append(categoria)
        if mes:
            consulta += " AND substr(fecha,1,7)=?"
            parametros.append(mes)
        with self.conexion() as con:
            return [Gasto(*fila) for fila in con.execute(consulta + " ORDER BY fecha DESC, id DESC", parametros)]

    def eliminar(self, id: int):
        with self.conexion() as con:
            cursor = con.execute("DELETE FROM gastos WHERE id=?", (id,))
            if cursor.rowcount != 1:
                raise ValueError("El gasto ya no existe.")
