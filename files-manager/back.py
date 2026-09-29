from __future__ import annotations

from pathlib import Path
import shutil

class Shell:

    def __init__(self, start_path: str | Path | None = None) -> None:
        self.cwd = Path(start_path or Path.home()).expanduser().resolve()
        if not self.cwd.is_dir():
            raise NotADirectoryError(self.cwd)

    def cd(self, route: str = "..") -> None:
        target = (self.cwd / route).resolve()
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
        return self.cwd.name or str(self.cwd)

    @staticmethod
    def _safe_name(name: str) -> str:
        clean = name.strip()
        if not clean or clean in {".", ".."} or Path(clean).name != clean:
            raise ValueError("Escribe un nombre válido, sin rutas.")
        return clean

    def mkdir(self, name: str) -> Path:
        target = self.cwd / self._safe_name(name)
        target.mkdir()
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
