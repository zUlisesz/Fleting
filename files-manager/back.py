from __future__ import annotations

from pathlib import Path
import shutil

class Shell:

    def __init__(self, start_path: str | Path | None = None) -> None:
        self.root = Path(start_path or Path.home()).expanduser().resolve()
        if not self.root.is_dir():
            raise NotADirectoryError(self.root)
        self.cwd = self.root

    def cd(self, route: str = "..") -> None:
        target = (self.cwd / route).resolve()
        if not target.is_relative_to(self.root):
            raise ValueError("No puedes salir de la carpeta inicial.")
        if not target.is_dir():
            raise NotADirectoryError(target)
        self.cwd = target

    def ls(self) -> list[Path]:
        """Return visible entries, with folders first and names sorted."""
        return sorted(
            (entry for entry in self.cwd.iterdir() if not entry.name.startswith(".")),
            key=lambda entry: (not entry.is_dir(), entry.name.casefold()),
        )

    def lsdir(self) -> list[Path]:
        return [entry for entry in self.ls() if entry.is_dir()]

    def relative_pwd(self) -> str:
        relative_path = self.cwd.relative_to(self.root)
        return str(relative_path) if relative_path.parts else self.root.name

    def can_go_up(self) -> bool:
        """Return whether the current directory has a parent within the session root."""
        return self.cwd != self.root

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
        """Rename one direct child without permitting paths outside the session root."""
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
        """Remove one child of the current directory (files or folders)."""
        target = self.cwd / self._safe_name(name)
        if target.parent != self.cwd or target == self.cwd:
            raise ValueError("Solo puedes quitar elementos de esta carpeta.")
        if target.is_symlink() or not target.is_dir():
            target.unlink()
        else:
            shutil.rmtree(target)
