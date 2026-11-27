"""Piezas de layout compartidas por todas las galerías."""

from collections.abc import Sequence

import flet as ft

Cols = dict[str, int]

CARD_COLS: Cols = {"xs": 12, "sm": 6, "md": 4}
WIDE_CARD_COLS: Cols = {"xs": 12, "sm": 6, "md": 4, "lg": 3}
TILE_COLS: Cols = {"xs": 6, "sm": 4, "md": 3, "lg": 2}


@ft.component
def ResponsiveGrid(
    children: Sequence[ft.Control],
    *,
    cols: Cols = CARD_COLS,
    spacing: int = 16,
) -> ft.Control:
    """Rejilla adaptable: cada hijo ocupa ``cols`` columnas según el ancho.

    ``col`` se aplica a un contenedor propio porque ``ResponsiveRow`` lo lee de
    sus hijos directos, y un componente no expone esa propiedad.
    """
    return ft.ResponsiveRow(
        spacing=spacing,
        run_spacing=spacing,
        controls=[ft.Container(col=cols, content=child) for child in children],
    )


@ft.component
def SampleCard(
    title: str,
    content: ft.Control,
    *,
    description: str = "",
    height: int | float | None = None,
) -> ft.Control:
    """Marco con título (y descripción opcional) alrededor de un ejemplo."""
    header: list[ft.Control] = [
        ft.Text(title, size=13, weight=ft.FontWeight.W_600),
    ]
    if description:
        header.append(
            ft.Text(description, size=12, color=ft.Colors.ON_SURFACE_VARIANT)
        )
    return ft.Container(
        height=height,
        padding=16,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=16,
        content=ft.Column(
            spacing=8,
            controls=[
                *header,
                ft.Container(
                    # ``expand`` exige una altura acotada: solo con ``height``.
                    expand=height is not None,
                    alignment=ft.Alignment.CENTER,
                    content=content,
                ),
            ],
        ),
    )


def sample_grid(
    samples: Sequence[tuple[str, str, ft.Control]],
    *,
    height: int | float | None = 200,
    cols: Cols = CARD_COLS,
) -> ft.Control:
    """Rejilla de ``SampleCard`` a partir de ``(título, descripción, control)``."""
    return ResponsiveGrid(
        [
            SampleCard(title, content, description=description, height=height, key=title)
            for title, description, content in samples
        ],
        cols=cols,
    )
