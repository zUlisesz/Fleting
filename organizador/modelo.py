"""Reglas y persistencia del organizador; no depende de Flet."""
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
import sqlite3

PRIORIDADES = ("Baja", "Media", "Alta")

@dataclass(frozen=True)
class Tarea:
    id: int
    titulo: str
    prioridad: str
    completada: bool


def validar(titulo: str, prioridad: str) -> str:
    titulo = titulo.strip()
    if not 1 <= len(titulo) <= 80:
        raise ValueError("El título debe tener entre 1 y 80 caracteres.")
    if prioridad not in PRIORIDADES:
        raise ValueError("Selecciona una prioridad válida.")
    return titulo


class Repositorio:
    def __init__(self, ruta: Path):
        self.ruta = Path(ruta)
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        with self.conexion() as con:
            con.execute("""CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY,
                titulo TEXT NOT NULL,
                prioridad TEXT NOT NULL CHECK(prioridad IN ('Baja','Media','Alta')),
                completada INTEGER NOT NULL DEFAULT 0 CHECK(completada IN (0,1)))""")

    @contextmanager
    def conexion(self):
        con = sqlite3.connect(self.ruta, timeout=10)
        try:
            with con:
                yield con
        finally:
            con.close()

    def listar(self, consulta="", estado="Todas") -> list[Tarea]:
        if estado not in ("Todas", "Pendientes", "Completadas"):
            raise ValueError("Filtro desconocido.")
        with self.conexion() as con:
            filas = con.execute("SELECT id, titulo, prioridad, completada FROM tareas ORDER BY id DESC").fetchall()
        tareas = [Tarea(id, titulo, prioridad, bool(completada)) for id, titulo, prioridad, completada in filas]
        texto = consulta.strip().casefold()
        return [t for t in tareas if texto in t.titulo.casefold() and
                (estado == "Todas" or t.completada == (estado == "Completadas"))]

    def agregar(self, titulo: str, prioridad: str) -> int:
        titulo = validar(titulo, prioridad)
        with self.conexion() as con:
            return con.execute("INSERT INTO tareas(titulo, prioridad) VALUES (?, ?)", (titulo, prioridad)).lastrowid

    def editar(self, id: int, titulo: str, prioridad: str):
        titulo = validar(titulo, prioridad)
        with self.conexion() as con:
            cursor = con.execute("UPDATE tareas SET titulo=?, prioridad=? WHERE id=?", (titulo, prioridad, id))
            if cursor.rowcount != 1:
                raise ValueError("La tarea ya no existe.")

    def completar(self, id: int, valor: bool):
        with self.conexion() as con:
            cursor = con.execute("UPDATE tareas SET completada=? WHERE id=?", (int(valor), id))
            if cursor.rowcount != 1:
                raise ValueError("La tarea ya no existe.")

    def eliminar(self, id: int):
        with self.conexion() as con:
            cursor = con.execute("DELETE FROM tareas WHERE id=?", (id,))
            if cursor.rowcount != 1:
                raise ValueError("La tarea ya no existe.")
