"""Botones con estilos variados, descritos como datos (``ButtonSpec``)."""

from dataclasses import dataclass

import flet as ft

from ._layout import WIDE_CARD_COLS, sample_grid


@dataclass(frozen=True)
class ButtonSpec:
    """Descripción visual de un botón; ``StyledButton`` la convierte en control."""

    text: str
    icon: ft.IconData | None = None
    color: str = "#FFFFFF"
    bgcolor: str = "#2563EB"
    hover_bgcolor: str | None = None
    radius: float = 10
    elevation: float = 0
    border_color: str | None = None
    border_width: float = 1
    padding: int = 18
    width: float | None = None
    height: float = 46
    shape: ft.OutlinedBorder | None = None
    disabled: bool = False


STYLES: tuple[tuple[str, ButtonSpec], ...] = (
    ("Primario", ButtonSpec("Continuar", ft.Icons.ARROW_FORWARD, hover_bgcolor="#1D4ED8")),
    (
        "Secundario",
        ButtonSpec(
            "Ver detalles", ft.Icons.VISIBILITY_OUTLINED,
            color="#334155", bgcolor="#F1F5F9", hover_bgcolor="#E2E8F0",
        ),
    ),
    (
        "Contorno",
        ButtonSpec(
            "Editar", ft.Icons.EDIT_OUTLINED,
            color="#2563EB", bgcolor="#FFFFFF", hover_bgcolor="#EFF6FF",
            border_color="#2563EB",
        ),
    ),
    (
        "Píldora",
        ButtonSpec(
            "Explorar", ft.Icons.EXPLORE_OUTLINED,
            bgcolor="#7C3AED", hover_bgcolor="#6D28D9",
            shape=ft.StadiumBorder(), padding=22,
        ),
    ),
    (
        "Éxito",
        ButtonSpec(
            "Completado", ft.Icons.CHECK_CIRCLE_OUTLINE,
            bgcolor="#16A34A", hover_bgcolor="#15803D",
        ),
    ),
    (
        "Alerta",
        ButtonSpec(
            "Eliminar", ft.Icons.DELETE_OUTLINE,
            bgcolor="#DC2626", hover_bgcolor="#B91C1C",
        ),
    ),
    (
        "Suave",
        ButtonSpec(
            "Favorito", ft.Icons.FAVORITE_BORDER,
            color="#BE185D", bgcolor="#FCE7F3", hover_bgcolor="#FBCFE8", radius=14,
        ),
    ),
    (
        "Oscuro",
        ButtonSpec(
            "Abrir consola", ft.Icons.TERMINAL,
            bgcolor="#0F172A", hover_bgcolor="#1E293B", radius=8, elevation=3,
        ),
    ),
    (
        "Neón",
        ButtonSpec(
            "Activar", ft.Icons.BOLT,
            color="#0F172A", bgcolor="#67E8F9", hover_bgcolor="#22D3EE",
            border_color="#0891B2", border_width=2, elevation=8, radius=14,
        ),
    ),
    (
        "Cálido",
        ButtonSpec(
            "Descubrir", ft.Icons.WB_SUNNY_OUTLINED,
            color="#431407", bgcolor="#FDBA74", hover_bgcolor="#FB923C", radius=16,
        ),
    ),
    (
        "Esquinas biseladas",
        ButtonSpec(
            "Construir", ft.Icons.HANDYMAN_OUTLINED,
            bgcolor="#4F46E5", hover_bgcolor="#4338CA",
            shape=ft.BeveledRectangleBorder(radius=10),
        ),
    ),
    (
        "Esquinas continuas",
        ButtonSpec(
            "Crear nuevo", ft.Icons.ADD,
            color="#3F3F46", bgcolor="#FAFAFA", hover_bgcolor="#F4F4F5",
            border_color="#A1A1AA", shape=ft.ContinuousRectangleBorder(radius=28),
        ),
    ),
    (
        "Compacto",
        ButtonSpec(
            "Filtrar", ft.Icons.FILTER_ALT_OUTLINED,
            color="#0F766E", bgcolor="#CCFBF1", hover_bgcolor="#99F6E4",
            height=36, padding=12, radius=8,
        ),
    ),
    (
        "Acción amplia",
        ButtonSpec(
            "Guardar cambios", ft.Icons.SAVE_OUTLINED,
            bgcolor="#0284C7", hover_bgcolor="#0369A1",
            width=210, height=52, radius=12, elevation=2,
        ),
    ),
    (
        "Monocromático",
        ButtonSpec(
            "Compartir", ft.Icons.SHARE_OUTLINED,
            color="#18181B", bgcolor="#FFFFFF", hover_bgcolor="#F4F4F5",
            border_color="#18181B", border_width=2, radius=0,
        ),
    ),
    (
        "Deshabilitado",
        ButtonSpec(
            "No disponible", ft.Icons.LOCK_OUTLINE,
            color="#64748B", bgcolor="#E2E8F0", disabled=True,
        ),
    ),
)


def spec_style(spec: ButtonSpec) -> ft.ButtonStyle:
    """Estilo de Flet con colores, sombra y forma por estado interactivo."""
    state = ft.ControlState
    hover = spec.hover_bgcolor or spec.bgcolor
    return ft.ButtonStyle(
        color={state.DEFAULT: spec.color, state.DISABLED: "#94A3B8"},
        bgcolor={
            state.DEFAULT: spec.bgcolor,
            state.HOVERED: hover,
            state.PRESSED: hover,
            state.DISABLED: "#E2E8F0",
        },
        elevation={
            state.DEFAULT: spec.elevation,
            state.HOVERED: spec.elevation + 4,
            state.PRESSED: 0,
        },
        padding=spec.padding,
        side=(
            ft.BorderSide(spec.border_width, spec.border_color)
            if spec.border_color
            else None
        ),
        shape=spec.shape or ft.RoundedRectangleBorder(radius=spec.radius),
        animation_duration=180,
        mouse_cursor=ft.MouseCursor.CLICK,
        text_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_600),
    )


@ft.component
def StyledButton(spec: ButtonSpec) -> ft.Control:
    """Botón construido a partir de un ``ButtonSpec``."""
    return ft.Button(
        content=spec.text,
        icon=spec.icon,
        disabled=spec.disabled,
        width=spec.width,
        height=spec.height,
        style=spec_style(spec),
    )


@ft.component
def StyledButtonsGallery() -> ft.Control:
    return sample_grid(
        [(title, "", StyledButton(spec)) for title, spec in STYLES],
        height=130,
        cols=WIDE_CARD_COLS,
    )
