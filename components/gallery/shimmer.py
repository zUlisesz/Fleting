"""Placeholders con efecto shimmer (skeletons de carga)."""

from collections.abc import Sequence

import flet as ft

from ..atoms import Button

DEFAULT_ITEMS: tuple[tuple[str, str], ...] = (
    ("Recent activity", "Smooth top-to-bottom sweep"),
    ("Monthly sales", "Waiting for the latest data"),
    ("New visitors", "Loading analytics"),
)

SHIMMER_GRADIENT = ft.LinearGradient(
    begin=ft.Alignment(-1.0, -0.5),
    end=ft.Alignment(1.0, 0.5),
    colors=[ft.Colors.PURPLE, ft.Colors.PURPLE, ft.Colors.AMBER_200, ft.Colors.PURPLE, ft.Colors.PURPLE],
    stops=[0.0, 0.35, 0.5, 0.65, 1.0],
)


def _line(width: int, height: int = 14) -> ft.Control:
    return ft.Container(
        width=width,
        height=height,
        bgcolor=ft.Colors.WHITE,
        opacity=0.6,
        border_radius=height,
    )


def _skeleton(title: str, subtitle: str, width: int) -> ft.Control:
    return ft.Container(
        width=width,
        padding=20,
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        border_radius=24,
        content=ft.Column(
            spacing=16,
            controls=[
                _line(max(80, width - 80)),
                ft.Row([_line(60, 10), _line(90, 10)], spacing=10),
                ft.Container(height=80, border_radius=16, bgcolor=ft.Colors.WHITE, opacity=0.35),
                ft.Column([_line(120, 12), _line(160, 12)], spacing=8),
                ft.Text(title, color=ft.Colors.WHITE, weight=ft.FontWeight.W_600),
                ft.Text(subtitle, color=ft.Colors.WHITE, size=12),
            ],
        ),
    )


def _loaded(title: str, subtitle: str, width: int) -> ft.Control:
    return ft.Container(
        width=width,
        height=330,
        padding=20,
        border_radius=24,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        content=ft.Column(
            controls=[
                ft.Text(title, weight=ft.FontWeight.W_600),
                ft.Text(subtitle, size=12, color=ft.Colors.ON_SURFACE_VARIANT),
            ]
        ),
    )


@ft.component
def ShimmerCard(
    title: str,
    subtitle: str,
    *,
    loading: bool = True,
    width: int = 220,
    period: int = 2200,
    gradient: ft.Gradient = SHIMMER_GRADIENT,
) -> ft.Control:
    """Tarjeta esqueleto con shimmer; con ``loading=False`` muestra el contenido."""
    if not loading:
        return _loaded(title, subtitle, width)
    return ft.Shimmer(
        gradient=gradient,
        direction=ft.ShimmerDirection.TTB,
        period=period,
        content=_skeleton(title, subtitle, width),
    )


@ft.component
def ShimmerGallery(
    items: Sequence[tuple[str, str]] = DEFAULT_ITEMS,
    *,
    width: int = 220,
    period: int = 2200,
) -> ft.Control:
    """Tarjetas shimmer con un botón que alterna entre cargando y cargado."""
    loading, set_loading = ft.use_state(True)
    return ft.Column(
        spacing=16,
        controls=[
            Button(
                "Mostrar contenido" if loading else "Volver a cargar",
                variant="outline",
                icon=ft.Icons.SWAP_HORIZ,
                on_click=lambda _: set_loading(not loading),
            ),
            ft.Row(
                wrap=True,
                spacing=16,
                run_spacing=16,
                controls=[
                    ShimmerCard(title, subtitle, loading=loading, width=width, period=period, key=title)
                    for title, subtitle in items
                ],
            ),
        ],
    )
