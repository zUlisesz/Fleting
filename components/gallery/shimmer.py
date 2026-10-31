"""Shimmer reutilizable para placeholders de tarjetas y galerías."""

from collections.abc import Sequence

import flet as ft


DEFAULT_SHIMMER_ITEMS = (
    ("Recent activity", "Smooth top-to-bottom sweep"),
    ("Monthly sales", "Waiting for the latest data"),
    ("New visitors", "Loading analytics"),
)


def _skeleton_line(width: int, height: int = 14) -> ft.Container:
    return ft.Container(
        width=width,
        height=height,
        bgcolor=ft.Colors.WHITE,
        opacity=0.6,
        border_radius=ft.BorderRadius.all(height),
    )


def _shimmer_content(title: str, subtitle: str, *, width: int = 220) -> ft.Container:
    return ft.Container(
        width=width,
        padding=ft.Padding.all(20),
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        border_radius=ft.BorderRadius.all(24),
        content=ft.Column(
            spacing=16,
            controls=[
                _skeleton_line(max(80, width - 80)),
                ft.Row(
                    spacing=10,
                    controls=[_skeleton_line(60, 10), _skeleton_line(90, 10)],
                ),
                ft.Container(
                    height=80,
                    border_radius=ft.BorderRadius.all(16),
                    bgcolor=ft.Colors.WHITE,
                    opacity=0.35,
                ),
                ft.Column(
                    spacing=8,
                    controls=[_skeleton_line(120, 12), _skeleton_line(160, 12)],
                ),
                ft.Text(title, color=ft.Colors.WHITE, weight=ft.FontWeight.W_600),
                ft.Text(subtitle, color=ft.Colors.WHITE, size=12),
            ],
        ),
    )


def shimmer_metric_card(
    title: str,
    subtitle: str,
    *,
    width: int = 220,
    period: int = 2200,
    gradient: ft.Gradient | None = None,
) -> ft.Shimmer:
    """Crea una tarjeta skeleton independiente y configurable."""

    gradient = gradient or ft.LinearGradient(
        begin=ft.Alignment(-1.0, -0.5),
        end=ft.Alignment(1.0, 0.5),
        colors=[ft.Colors.PURPLE, ft.Colors.PURPLE, ft.Colors.AMBER_200, ft.Colors.PURPLE, ft.Colors.PURPLE],
        stops=[0.0, 0.35, 0.5, 0.65, 1.0],
    )
    return ft.Shimmer(
        gradient=gradient,
        direction=ft.ShimmerDirection.TTB,
        period=period,
        content=_shimmer_content(title, subtitle, width=width),
    )


def shimmer_gallery(
    items: Sequence[tuple[str, str]] = DEFAULT_SHIMMER_ITEMS,
    *,
    width: int = 220,
    period: int = 2200,
) -> ft.Row:
    """Construye una galería de placeholders a partir de cualquier colección."""

    return ft.Row(
        wrap=True,
        spacing=16,
        run_spacing=16,
        controls=[
            shimmer_metric_card(title, subtitle, width=width, period=period)
            for title, subtitle in items
        ],
    )


def main(page: ft.Page) -> None:
    """Demo independiente del shimmer."""

    page.title = "Shimmer - reusable gallery"
    page.bgcolor = "#0E0E18"
    page.add(shimmer_gallery())


if __name__ == "__main__":
    ft.run(main)

