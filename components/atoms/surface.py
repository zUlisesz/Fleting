"""Container estilizado mínimo para agrupar componentes reutilizables."""

import flet as ft

from theme import COLORS


def surface(
    content: ft.Control,
    *,
    padding: int | float = 24,
    radius: int | float = 14,
    bgcolor: str | None = None,
    width: int | float | None = None,
    height: int | float | None = None,
) -> ft.Container:
    """Crea una superficie oscura consistente para galerías y demos."""

    return ft.Container(
        width=width,
        height=height,
        padding=padding,
        bgcolor=bgcolor or COLORS.surface,
        border=ft.Border.all(1, COLORS.border),
        border_radius=radius,
        content=content,
    )
