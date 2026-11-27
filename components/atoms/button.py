"""Botón con texto, inspirado en shadcn/ui."""

from collections.abc import Callable
from typing import Literal

import flet as ft

from ..theme import COLORS

Variant = Literal["default", "outline"]
VARIANTS: tuple[Variant, ...] = ("default", "outline")


def button_style(variant: Variant) -> ft.ButtonStyle:
    """Estilo (colores por estado, forma y relleno) de cada variante."""
    if variant not in VARIANTS:
        raise ValueError(f"variant debe ser uno de {VARIANTS}, no {variant!r}")

    filled = variant == "default"
    text = COLORS.surface if filled else COLORS.text
    state = ft.ControlState
    return ft.ButtonStyle(
        color={
            state.DEFAULT: text,
            state.HOVERED: text,
            state.DISABLED: COLORS.placeholder,
        },
        bgcolor={
            state.DEFAULT: COLORS.accent if filled else COLORS.surface,
            state.HOVERED: COLORS.accent_hover if filled else COLORS.background,
            state.DISABLED: COLORS.border,
        },
        side=None if filled else ft.BorderSide(width=1, color=COLORS.border),
        shape=ft.RoundedRectangleBorder(radius=8),
        padding=ft.Padding.symmetric(horizontal=16, vertical=10),
        elevation=0,
        animation_duration=120,
    )


@ft.component
def Button(
    label: str,
    *,
    on_click: Callable[..., None] | None = None,
    variant: Variant = "default",
    icon: ft.IconData | None = None,
    disabled: bool = False,
) -> ft.Control:
    """Botón ``default`` (relleno) u ``outline`` (contorno).

    >>> Button("Guardar", icon=ft.Icons.SAVE, on_click=lambda _: guardar())
    """
    control = ft.FilledButton if variant == "default" else ft.OutlinedButton
    return control(
        content=label,
        icon=icon,
        style=button_style(variant),
        on_click=on_click,
        disabled=disabled,
    )
