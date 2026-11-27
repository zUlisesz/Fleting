"""Persistencia SQLite de perfiles y movimientos."""

from __future__ import annotations

import os
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from .dominio import (
    CATEGORIAS,
    TIPOS,
    Filtros,
    Movimiento,
    a_centavos,
    validar_fecha,
    validar_texto,
)

PERFIL_INICIAL = (1, "Ulises")


def _validar_id(valor: object, nombre: str) -> int:
    if type(valor) is not int:
        raise ValueError(f"El {nombre} no es válido.")
    return valor


class Repositorio:
    """Guarda movimientos por perfil; migra la tabla antigua ``gastos``.

    Los métodos reciben el ``perfil_id`` explícitamente: el repositorio no
    guarda ninguna selección, así que es seguro compartirlo entre componentes.
    """

    def __init__(self, ruta: Path) -> None:
        self.ruta = Path(ruta)
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        with self.conexion(claves_foraneas=False) as con:
            con.execute("BEGIN IMMEDIATE")
            self._preparar_esquema(con)

    @contextmanager
    def conexion(self, *, claves_foraneas: bool = True) -> Iterator[sqlite3.Connection]:
        con = sqlite3.connect(self.ruta, timeout=10)
        try:
            con.execute(f"PRAGMA foreign_keys={'ON' if claves_foraneas else 'OFF'}")
            with con:
                yield con
        finally:
            con.close()

    @staticmethod
    def _preparar_esquema(con: sqlite3.Connection) -> None:
        tablas = {fila[0] for fila in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        con.execute(
            "CREATE TABLE IF NOT EXISTS perfiles ("
            "id INTEGER PRIMARY KEY, nombre TEXT NOT NULL COLLATE NOCASE UNIQUE)"
        )
        con.execute("INSERT OR IGNORE INTO perfiles(id, nombre) VALUES (?, ?)", PERFIL_INICIAL)
        con.execute(
            """CREATE TABLE IF NOT EXISTS movimientos (
                id INTEGER PRIMARY KEY,
                fecha TEXT NOT NULL,
                concepto TEXT NOT NULL,
                categoria TEXT NOT NULL,
                tipo TEXT NOT NULL CHECK(tipo IN ('Gasto', 'Ingreso')),
                centavos INTEGER NOT NULL CHECK(centavos > 0))"""
        )
        if "gastos" in tablas and "movimientos" not in tablas:
            con.execute(
                """INSERT INTO movimientos(id, fecha, concepto, categoria, tipo, centavos)
                   SELECT id, fecha, concepto, categoria, 'Gasto', centavos FROM gastos"""
            )
        columnas = {fila[1] for fila in con.execute("PRAGMA table_info(movimientos)")}
        if "perfil_id" not in columnas:
            con.execute(
                "ALTER TABLE movimientos ADD COLUMN perfil_id INTEGER NOT NULL DEFAULT 1 "
                "REFERENCES perfiles(id)"
            )
        for columna in ("perfil_id", "fecha", "tipo"):
            con.execute(f"CREATE INDEX IF NOT EXISTS idx_movimientos_{columna} ON movimientos({columna})")

    # Perfiles 
    def perfiles(self) -> list[tuple[int, str]]:
        with self.conexion() as con:
            return con.execute("SELECT id, nombre FROM perfiles ORDER BY nombre COLLATE NOCASE").fetchall()

    def crear_perfil(self, nombre: str) -> int:
        nombre = validar_texto(nombre, "nombre")
        try:
            with self.conexion() as con:
                return con.execute("INSERT INTO perfiles(nombre) VALUES (?)", (nombre,)).lastrowid
        except sqlite3.IntegrityError as error:
            raise ValueError("Ya existe un perfil con ese nombre.") from error

    def existe_perfil(self, perfil_id: int) -> bool:
        _validar_id(perfil_id, "perfil seleccionado")
        with self.conexion() as con:
            return con.execute("SELECT 1 FROM perfiles WHERE id=?", (perfil_id,)).fetchone() is not None

    # Movimientos
    def agregar(
        self, perfil_id: int, fecha: str, concepto: str, categoria: str, tipo: str, importe: str
    ) -> int:
        _validar_id(perfil_id, "perfil seleccionado")
        fecha = validar_fecha(fecha)
        concepto = validar_texto(concepto, "concepto")
        if categoria not in CATEGORIAS:
            raise ValueError("Selecciona una categoría válida.")
        if tipo not in TIPOS:
            raise ValueError("Selecciona un tipo de movimiento válido.")
        centavos = a_centavos(importe)
        try:
            with self.conexion() as con:
                return con.execute(
                    "INSERT INTO movimientos(fecha, concepto, categoria, tipo, centavos, perfil_id) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (fecha, concepto, categoria, tipo, centavos, perfil_id),
                ).lastrowid
        except sqlite3.IntegrityError as error:
            raise ValueError("El perfil no existe.") from error

    def listar(self, perfil_id: int, filtros: Filtros = Filtros()) -> list[Movimiento]:
        _validar_id(perfil_id, "perfil seleccionado")
        filtros.validar()
        consulta = "SELECT id, fecha, concepto, categoria, tipo, centavos FROM movimientos WHERE perfil_id=?"
        parametros: list[object] = [perfil_id]
        if filtros.categoria != "Todas":
            consulta += " AND categoria=?"
            parametros.append(filtros.categoria)
        if filtros.mes:
            consulta += " AND substr(fecha, 1, 7)=?"
            parametros.append(filtros.mes)
        if filtros.tipo != "Todos":
            consulta += " AND tipo=?"
            parametros.append(filtros.tipo)
        with self.conexion() as con:
            filas = con.execute(consulta + " ORDER BY fecha DESC, id DESC", parametros).fetchall()
        return [Movimiento(*fila) for fila in filas]

    def eliminar(self, perfil_id: int, movimiento_id: int) -> None:
        _validar_id(perfil_id, "perfil seleccionado")
        with self.conexion() as con:
            cursor = con.execute(
                "DELETE FROM movimientos WHERE id=? AND perfil_id=?", (movimiento_id, perfil_id)
            )
            if cursor.rowcount != 1:
                raise ValueError("El movimiento ya no existe.")


def ruta_por_defecto() -> Path:
    """``$FLET_DATA_DIR/finanzas.sqlite3`` o ``~/.fletBD/finanzas.sqlite3``."""
    base = os.environ.get("FLET_DATA_DIR") or str(Path.home() / ".fletBD")
    return Path(base) / "finanzas.sqlite3"
