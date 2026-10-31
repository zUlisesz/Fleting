"""Tokens visuales compartidos por los componentes del ejemplo."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Palette:
    """Paleta mínima inspirada en los colores neutros de shadcn/ui."""

    background: str = "#FAFAFA"
    surface: str = "#FFFFFF"
    border: str = "#E4E4E7"
    muted: str = "#71717A"
    placeholder: str = "#A1A1AA"
    text: str = "#18181B"
    text_secondary: str = "#3F3F46"
    accent: str = "#18181B"
    accent_hover: str = "#3F3F46"


COLORS = Palette()

