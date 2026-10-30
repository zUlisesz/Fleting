"""Botones atómicos con apariencia inspirada en shadcn/ui."""

from collections.abc import Callable

import flet as ft

from theme import COLORS


def shadcn_button(
    label: str,
    *,
    on_click: Callable[..., None] | None = None,
    variant: str = "default",
    icon: ft.IconData | None = None,
    disabled: bool = False,
) -> ft.Control:
    """Crea un botón ``default`` u ``outline`` reutilizable."""

    if variant not in {"default", "outline"}:
        raise ValueError("variant debe ser 'default' o 'outline'")

    is_default = variant == "default"
    style = ft.ButtonStyle(
        color={
            ft.ControlState.DEFAULT: COLORS.surface if is_default else COLORS.text,
            ft.ControlState.HOVERED: COLORS.surface if is_default else COLORS.text,
            ft.ControlState.DISABLED: COLORS.placeholder,
        },
        bgcolor={
            ft.ControlState.DEFAULT: COLORS.accent if is_default else COLORS.surface,
            ft.ControlState.HOVERED: COLORS.accent_hover if is_default else COLORS.background,
            ft.ControlState.DISABLED: COLORS.border,
        },
        side=ft.BorderSide(width=1, color=COLORS.border) if not is_default else None,
        shape=ft.RoundedRectangleBorder(radius=8),
        padding=ft.Padding.symmetric(horizontal=16, vertical=10),
        elevation=0,
        animation_duration=120,
    )

    button_class = ft.FilledButton if is_default else ft.OutlinedButton
    return button_class(
        content=label,
        icon=icon,
        style=style,
        on_click=on_click,
        disabled=disabled,
    )

