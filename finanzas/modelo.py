"""Reglas de dominio y persistencia SQLite para el control de movimientos."""
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
import re
import sqlite3

CATEGORIAS = ("Comida", "Transporte", "Estudio", "Hogar", "Ocio", "Ahorro", "Trabajo", "Otros")
TIPOS = ("Gasto", "Ingreso")
TIPOS_FILTRO = ("Todos", *TIPOS)


def a_centavos(texto: str) -> int:
    """Convierte un importe positivo con hasta dos decimales a centavos."""
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
    """Formatea centavos como importe absoluto en pesos mexicanos."""
    centavos = abs(centavos)
    return f"${centavos // 100:,}.{centavos % 100:02d}"


def moneda_firmada(centavos: int) -> str:
    """Formatea un saldo conservando el signo deudor cuando existe."""
    signo = "-" if centavos < 0 else ""
    return f"{signo}{moneda(centavos)}"


@dataclass(frozen=True)
class Movimiento:
    id: int
    fecha: str
    concepto: str
    categoria: str
    tipo: str
    centavos: int


def resumir(movimientos: list[Movimiento]) -> dict:
    """Calcula totales de flujo de efectivo para un conjunto de movimientos."""
    categorias = {}
    ingresos = 0
    gastos = 0
    for movimiento in movimientos:
        category_key = f"{movimiento.tipo} · {movimiento.categoria}"
        categorias[category_key] = categorias.get(category_key, 0) + movimiento.centavos
        if movimiento.tipo == "Ingreso":
            ingresos += movimiento.centavos
        else:
            gastos += movimiento.centavos
    return {
        "total": ingresos + gastos,
        "cantidad": len(movimientos),
        "categorias": categorias,
        "ingresos": ingresos,
        "gastos": gastos,
        "balance": ingresos - gastos,
    }


class Repositorio:
    """Persistencia local de movimientos, con migración desde la tabla antigua."""

    def __init__(self, ruta: Path):
        self.ruta = Path(ruta)
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        with self.conexion() as con:
            con.execute("BEGIN IMMEDIATE")
            self._preparar_esquema(con)
        self.perfil_id = 1

    @contextmanager
    def conexion(self):
        con = sqlite3.connect(self.ruta, timeout=10)
        try:
            with con:
                yield con
        finally:
            con.close()

    @staticmethod
    def _preparar_esquema(con: sqlite3.Connection):
        tablas = {fila[0] for fila in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        con.execute("CREATE TABLE IF NOT EXISTS perfiles (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL COLLATE NOCASE UNIQUE)")
        con.execute("INSERT OR IGNORE INTO perfiles(id, nombre) VALUES (1, 'Ulises')")
        con.execute("""CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY,
            fecha TEXT NOT NULL,
            concepto TEXT NOT NULL,
            categoria TEXT NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('Gasto', 'Ingreso')),
            centavos INTEGER NOT NULL CHECK(centavos > 0))""")
        if "gastos" in tablas and "movimientos" not in tablas:
            con.execute("""INSERT INTO movimientos(id, fecha, concepto, categoria, tipo, centavos)
                SELECT id, fecha, concepto, categoria, 'Gasto', centavos FROM gastos""")
        if "perfil_id" not in {fila[1] for fila in con.execute("PRAGMA table_info(movimientos)")}:
            con.execute("ALTER TABLE movimientos ADD COLUMN perfil_id INTEGER NOT NULL DEFAULT 1 REFERENCES perfiles(id)")
        con.execute("CREATE INDEX IF NOT EXISTS idx_movimientos_perfil ON movimientos(perfil_id)")
        con.execute("CREATE INDEX IF NOT EXISTS idx_movimientos_fecha ON movimientos(fecha)")
        con.execute("CREATE INDEX IF NOT EXISTS idx_movimientos_tipo ON movimientos(tipo)")

    def perfiles(self):
        with self.conexion() as con:
            return con.execute("SELECT id, nombre FROM perfiles ORDER BY nombre COLLATE NOCASE").fetchall()

    def crear_perfil(self, nombre):
        nombre = nombre.strip()
        if not 1 <= len(nombre) <= 80:
            raise ValueError("El nombre debe tener entre 1 y 80 caracteres.")
        try:
            with self.conexion() as con:
                return con.execute("INSERT INTO perfiles(nombre) VALUES (?)", (nombre,)).lastrowid
        except sqlite3.IntegrityError as error:
            raise ValueError("Ya existe un perfil con ese nombre.") from error

    def seleccionar_perfil(self, perfil_id):
        with self.conexion() as con:
            if not con.execute("SELECT 1 FROM perfiles WHERE id=?", (perfil_id,)).fetchone():
                raise ValueError("El perfil no existe.")
        self.perfil_id = perfil_id

    def agregar(self, fecha: str, concepto: str, categoria: str, tipo: str, importe: str) -> int:
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
            return con.execute(
                "INSERT INTO movimientos(fecha, concepto, categoria, tipo, centavos, perfil_id) VALUES (?, ?, ?, ?, ?, ?)",
                (fecha, concepto, categoria, tipo, centavos, self.perfil_id),
            ).lastrowid

    def listar(self, categoria="Todas", mes="", tipo="Todos") -> list[Movimiento]:
        if categoria != "Todas" and categoria not in CATEGORIAS:
            raise ValueError("Categoría de filtro inválida.")
        if tipo not in TIPOS_FILTRO:
            raise ValueError("Tipo de filtro inválido.")
        if mes:
            if not re.fullmatch(r"\d{4}-\d{2}", mes):
                raise ValueError("El mes debe tener formato AAAA-MM.")
            try:
                date.fromisoformat(mes + "-01")
            except ValueError as error:
                raise ValueError("Mes inválido.") from error

        consulta = "SELECT id, fecha, concepto, categoria, tipo, centavos FROM movimientos WHERE perfil_id=?"
        parametros = [self.perfil_id]
        if categoria != "Todas":
            consulta += " AND categoria=?"
            parametros.append(categoria)
        if mes:
            consulta += " AND substr(fecha, 1, 7)=?"
            parametros.append(mes)
        if tipo != "Todos":
            consulta += " AND tipo=?"
            parametros.append(tipo)
        with self.conexion() as con:
            filas = con.execute(consulta + " ORDER BY fecha DESC, id DESC", parametros)
            return [Movimiento(*fila) for fila in filas]

    def _total_por_tipo(self, tipo: str) -> int:
        with self.conexion() as con:
            fila = con.execute(
                "SELECT COALESCE(SUM(centavos), 0) FROM movimientos WHERE tipo=? AND perfil_id=?", (tipo, self.perfil_id)
            ).fetchone()
        return int(fila[0])

    def gastos(self) -> int:
        return self._total_por_tipo("Gasto")

    def ingresos(self) -> int:
        return self._total_por_tipo("Ingreso")

    def eliminar(self, id: int):
        with self.conexion() as con:
            cursor = con.execute("DELETE FROM movimientos WHERE id=? AND perfil_id=?", (id, self.perfil_id))
            if cursor.rowcount != 1:
                raise ValueError("El movimiento ya no existe.")
