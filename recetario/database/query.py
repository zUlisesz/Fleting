"""Ejecución de consultas: una conexión por llamada y errores del driver unificados.

Los repositorios solo describen SQL y parámetros; aquí vive el manejo de
conexiones, cursores y transacciones.
"""

from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from typing import Any

import mysql.connector

from .config import get_connection

Params = Sequence[Any]
Row = dict[str, Any]


class StorageError(Exception):
    """No se pudo completar una operación con la base de datos."""


@contextmanager
def _cursor(*, dictionary: bool, commit: bool = False) -> Iterator[Any]:
    try:
        with get_connection() as connection:
            with connection.cursor(dictionary=dictionary) as cursor:
                yield cursor
            if commit:
                connection.commit()
    except mysql.connector.Error as error:
        raise StorageError(f"Error de base de datos: {error}") from error


def fetch_all(query: str, params: Params = ()) -> list[Row]:
    with _cursor(dictionary=True) as cursor:
        cursor.execute(query, tuple(params))
        return cursor.fetchall()


def fetch_one(query: str, params: Params = ()) -> Row | None:
    with _cursor(dictionary=True) as cursor:
        cursor.execute(query, tuple(params))
        return cursor.fetchone()


def execute(query: str, params: Params = ()) -> int:
    """Ejecuta un INSERT/UPDATE/DELETE y devuelve las filas afectadas."""
    with _cursor(dictionary=False, commit=True) as cursor:
        cursor.execute(query, tuple(params))
        return cursor.rowcount
