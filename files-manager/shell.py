"""Operaciones de archivos acotadas a la carpeta inicial"""

from __future__ import annotations

import shutil
from pathlib import Path


def describe(path: Path) -> str:
    """Texto corto para mostrar bajo el nombre: ``Carpeta`` o el tamaño en bytes."""
    try:
        return "Carpeta" if path.is_dir() else f"{path.stat().st_size:,} bytes"
    except OSError:
        return "No disponible"


def match_name(entries: list[Path], query: str) -> list[Path]:
    """Entradas cuyo nombre contiene ``query`` (sin distinguir mayúsculas).

    Una consulta vacía o en blanco no filtra nada.
    """
    term = query.strip().casefold()
    return [entry for entry in entries if term in entry.name.casefold()]


class Shell:
    """Sesión de navegación limitada a ``root``: no se puede salir de esa carpeta."""

    def __init__(self, start_path: str | Path | None = None) -> None:
        source = Path.home() if start_path is None else start_path
        try:
            self.root = Path(source).expanduser().resolve()
        except (TypeError, ValueError) as error:
            raise ValueError("La carpeta inicial no es válida.") from error
        if not self.root.is_dir():
            raise NotADirectoryError(self.root)
        self.cwd = self.root

    # Navegación
    def cd(self, route: str = "..") -> None:
        if not isinstance(route, str):
            raise ValueError("La ruta debe ser texto.")
        target = (self.cwd / route).resolve()
        if not target.is_relative_to(self.root):
            raise ValueError("No puedes salir de la carpeta inicial.")
        if not target.is_dir():
            raise NotADirectoryError(target)
        self.cwd = target

    def can_go_up(self) -> bool:
        """Indica si hay un nivel superior dentro de la carpeta inicial."""
        return self.cwd != self.root

    def relative_pwd(self) -> str:
        relative_path = self.cwd.relative_to(self.root)
        return str(relative_path) if relative_path.parts else self.root.name

    # Consulta
    def ls(self) -> list[Path]:
        """Entradas visibles de la carpeta actual: primero carpetas, por nombre."""
        return sorted(
            (entry for entry in self.cwd.iterdir() if not entry.name.startswith(".")),
            key=lambda entry: (not entry.is_dir(), entry.name.casefold()),
        )

    def lsdir(self) -> list[Path]:
        return [entry for entry in self.ls() if entry.is_dir()]

    def search(self, query: str) -> list[Path]:
        """Busca por nombre **solo** entre los elementos directos de la carpeta actual.

        No desciende a subcarpetas ni mira fuera de ``cwd``: un archivo dentro
        de otra carpeta (superior, hermana o interior) nunca aparece.
        """
        if not isinstance(query, str):
            raise ValueError("La búsqueda debe ser texto.")
        return match_name(self.ls(), query)

    # Modificación
    @staticmethod
    def _safe_name(name: str) -> str:
        if not isinstance(name, str):
            raise ValueError("Escribe un nombre válido, sin rutas.")
        clean = name.strip()
        if not clean or clean in {".", ".."} or Path(clean).name != clean:
            raise ValueError("Escribe un nombre válido, sin rutas.")
        return clean

    def mkdir(self, name: str) -> Path:
        target = self.cwd / self._safe_name(name)
        target.mkdir()
        return target

    def rename(self, current_name: str, new_name: str) -> Path:
        """Renombra un elemento directo sin permitir rutas fuera de la carpeta actual."""
        source = self.cwd / self._safe_name(current_name)
        target = self.cwd / self._safe_name(new_name)
        if source == target:
            raise ValueError("El nombre nuevo debe ser diferente.")
        if not source.exists() and not source.is_symlink():
            raise FileNotFoundError(source)
        if target.exists() or target.is_symlink():
            raise FileExistsError(target)
        source.rename(target)
        return target

    def rm(self, name: str) -> None:
        """Elimina un elemento directo de la carpeta actual (archivo o carpeta)."""
        target = self.cwd / self._safe_name(name)
        if target.parent != self.cwd or target == self.cwd:
            raise ValueError("Solo puedes quitar elementos de esta carpeta.")
        if target.is_symlink() or not target.is_dir():
            target.unlink()
        else:
            shutil.rmtree(target)
