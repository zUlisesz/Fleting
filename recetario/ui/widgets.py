"""Piezas visuales pequeñas y reutilizables."""

from collections.abc import Callable
from dataclasses import dataclass

import flet as ft

from . import theme


@dataclass(frozen=True, eq=False)
class Notice:
    """Mensaje breve (snackbar). ``eq=False``: cada aviso es distinto aunque repita el texto."""

    text: str
    error: bool = False


@ft.component
def Toast(notice: Notice, *, on_dismiss: Callable[[], None]) -> ft.Control:
    """Muestra el aviso mientras el componente esté montado."""
    ft.use_dialog(
        ft.SnackBar(
            content=ft.Text(notice.text, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500),
            bgcolor=theme.DANGER if notice.error else theme.SUCCESS,
            duration=3000,
            on_dismiss=lambda _: on_dismiss(),
        )
    )
    return ft.Container(visible=False)


@ft.component
def EmptyHint(text: str) -> ft.Control:
    return ft.Container(
        padding=16,
        alignment=ft.Alignment.CENTER,
        content=ft.Text(
            text,
            size=13,
            color=theme.FAINT,
            italic=True,
            text_align=ft.TextAlign.CENTER,
        ),
    )


@ft.component
def CountBadge(count: int, *, bgcolor: str, color: str) -> ft.Control:
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=8, vertical=2),
        bgcolor=bgcolor,
        border_radius=10,
        content=ft.Text(str(count), size=11, weight=ft.FontWeight.BOLD, color=color),
    )


@ft.component
def SectionCard(
    title: str,
    *,
    icon: ft.IconData,
    icon_color: str,
    count: int,
    badge_bgcolor: str,
    badge_color: str,
    action_label: str,
    on_action: Callable[[], None],
    spacing: int,
    children: list[ft.Control],
) -> ft.Control:
    """Tarjeta con encabezado (icono, título, contador, botón de acción) y contenido."""
    return ft.Card(
        elevation=0.5,
        bgcolor=ft.Colors.GREY_100,
        shape=ft.RoundedRectangleBorder(radius=14),
        content=ft.Container(
            padding=16,
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                spacing=8,
                                controls=[
                                    ft.Icon(icon, size=20, color=icon_color),
                                    ft.Text(
                                        title,
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color=theme.TEXT,
                                    ),
                                    CountBadge(count, bgcolor=badge_bgcolor, color=badge_color),
                                ],
                            ),
                            ft.FilledButton(
                                content=ft.Text(action_label, size=12),
                                icon=ft.Icons.ADD,
                                height=32,
                                bgcolor=theme.ACCENT_DARK,
                                on_click=lambda _: on_action(),
                            ),
                        ],
                    ),
                    ft.Column(spacing=spacing, controls=children),
                ],
            ),
        ),
    )
