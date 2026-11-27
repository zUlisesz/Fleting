"""Acceso a MySQL: configuración de la conexión y consultas."""

from .query import StorageError, execute, fetch_all, fetch_one

__all__ = ["StorageError", "execute", "fetch_all", "fetch_one"]
