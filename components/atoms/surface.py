"""Superficie con borde y esquinas redondeadas para agrupar contenido."""

import flet as ft

from ..theme import COLORS


@ft.component
def Surface(
    content: ft.Control,
    *,
    padding: int | float = 24,
    radius: int | float = 14,
    bgcolor: str | None = None,
    width: int | float | None = None,
    height: int | float | None = None,
) -> ft.Control:
    """Agrupa ``content`` sobre un fondo con borde fino."""
    return ft.Container(
        width=width,
        height=height,
        padding=padding,
        bgcolor=bgcolor or COLORS.surface,
        border=ft.Border.all(1, COLORS.border),
        border_radius=radius,
        content=content,
    )
