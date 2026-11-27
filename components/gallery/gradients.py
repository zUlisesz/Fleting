"""Gradientes lineales, radiales y angulares."""

import math
from dataclasses import dataclass

import flet as ft

from ..atoms import Button
from ._layout import ResponsiveGrid

A = ft.Alignment
GROUPS = ("Todos", "Linear", "Radial", "Sweep", "Neon")


@dataclass(frozen=True)
class GradientSpec:
    name: str
    gradient: ft.Gradient

    @property
    def group(self) -> str:
        """Primera palabra del nombre: ``"Linear · ocean"`` → ``"Linear"``."""
        return self.name.split(" · ")[0]


def _linear(name, begin, end, colors, stops=None) -> GradientSpec:
    return GradientSpec(name, ft.LinearGradient(begin=begin, end=end, colors=colors, stops=stops))


def _radial(name, colors, *, center=A.CENTER, radius=0.9, stops=None, **extra) -> GradientSpec:
    return GradientSpec(
        name,
        ft.RadialGradient(center=center, radius=radius, colors=colors, stops=stops, **extra),
    )


def _sweep(name, colors, *, stops=None, **extra) -> GradientSpec:
    return GradientSpec(name, ft.SweepGradient(center=A.CENTER, colors=colors, stops=stops, **extra))


GRADIENTS: tuple[GradientSpec, ...] = (
    _linear("Linear · horizontal", A.CENTER_LEFT, A.CENTER_RIGHT, ["#2563EB", "#7C3AED"]),
    _linear("Linear · vertical", A.TOP_CENTER, A.BOTTOM_CENTER, ["#F97316", "#DB2777"]),
    _linear("Linear · multicolor", A.TOP_LEFT, A.BOTTOM_RIGHT, ["#06B6D4", "#22C55E", "#EAB308"], [0.0, 0.45, 1.0]),
    _linear("Linear · sunset", A.TOP_LEFT, A.BOTTOM_RIGHT, ["#FDE68A", "#FB7185", "#7C3AED"]),
    _linear("Linear · ocean", A.TOP_CENTER, A.BOTTOM_CENTER, ["#A5F3FC", "#0891B2", "#164E63"]),
    _linear("Linear · forest", A.CENTER_LEFT, A.CENTER_RIGHT, ["#D9F99D", "#65A30D", "#14532D"]),
    _linear("Linear · rose gold", A.BOTTOM_LEFT, A.TOP_RIGHT, ["#9F1239", "#FDA4AF", "#FDE68A"], [0.0, 0.55, 1.0]),
    _linear("Neon · purple blue", A.TOP_LEFT, A.BOTTOM_RIGHT, ["#D946EF", "#7C3AED", "#2563EB", "#22D3EE"], [0.0, 0.32, 0.7, 1.0]),
    _linear("Neon · cyan green", A.CENTER_LEFT, A.CENTER_RIGHT, ["#00F5FF", "#00FFB3", "#A3FF12"]),
    _linear("Neon · yellow red", A.TOP_CENTER, A.BOTTOM_CENTER, ["#F9FF00", "#FF8A00", "#FF1744"]),
    _linear("Neon · galaxy", A.BOTTOM_LEFT, A.TOP_RIGHT, ["#090026", "#4C1D95", "#E040FB", "#00D9FF"], [0.0, 0.38, 0.72, 1.0]),
    _radial("Radial · centered", ["#FDE68A", "#F97316", "#9A3412"], radius=0.8, stops=[0.0, 0.45, 1.0]),
    _radial("Radial · offset", ["#F0ABFC", "#A855F7", "#312E81"], center=A(-0.5, -0.5), radius=1.1),
    _radial("Radial · focal", ["#FFFFFF", "#38BDF8", "#0C4A6E"], radius=0.85, focal=A(-0.4, -0.3), focal_radius=0.1),
    _radial("Radial · lavender", ["#F5D0FE", "#C084FC", "#6D28D9"]),
    _radial("Radial · ember", ["#FEF08A", "#F97316", "#7F1D1D"], center=A(0.4, 0.3), radius=1.0),
    _radial("Radial · mint", ["#ECFDF5", "#5EEAD4", "#0F766E"], center=A(-0.3, -0.4), radius=0.95),
    _radial("Radial · midnight", ["#818CF8", "#4338CA", "#0F172A"], radius=0.85, stops=[0.0, 0.5, 1.0]),
    _radial("Neon · violet pulse", ["#F0ABFC", "#A21CAF", "#3B0764", "#090026"], stops=[0.0, 0.28, 0.65, 1.0]),
    _radial("Neon · electric lagoon", ["#CCFFF6", "#00F5D4", "#008CFF", "#071B4D"], center=A(-0.35, -0.35), radius=1.1, stops=[0.0, 0.3, 0.68, 1.0]),
    _radial("Neon · solar flare", ["#FFFFFF", "#F9FF00", "#FF5A00", "#7F001D"], center=A(0.2, -0.2), radius=1.0, stops=[0.0, 0.2, 0.55, 1.0]),
    _radial("Neon · nebula", ["#FF67F0", "#6D28D9", "#1D4ED8", "#08071C"], center=A(-0.2, 0.2), radius=1.0, stops=[0.0, 0.3, 0.7, 1.0]),
    _sweep("Sweep · spectrum", ["#EF4444", "#FACC15", "#22C55E", "#3B82F6", "#A855F7", "#EF4444"], stops=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0]),
    _sweep("Sweep · rotated", ["#0F172A", "#2DD4BF", "#F8FAFC", "#0F172A"], stops=[0.0, 0.35, 0.7, 1.0], rotation=math.pi / 4),
    _sweep("Sweep · half turn", ["#FB7185", "#FBBF24", "#7C3AED"], stops=[0.0, 0.5, 1.0], start_angle=0.0, end_angle=math.pi),
    _sweep("Sweep · citrus", ["#F97316", "#FACC15", "#84CC16", "#F97316"]),
    _sweep("Sweep · lagoon", ["#0F766E", "#67E8F9", "#2563EB", "#0F766E"]),
    _sweep("Sweep · berry", ["#881337", "#F472B6", "#A855F7", "#881337"]),
    _sweep("Sweep · copper", ["#78350F", "#FBBF24", "#FED7AA", "#78350F"], rotation=math.pi / 3),
    _sweep("Neon · ultraviolet", ["#6D28D9", "#F000FF", "#00D9FF", "#2563EB", "#6D28D9"]),
    _sweep("Neon · acid green", ["#00F5FF", "#00FF85", "#D8FF00", "#00F5FF"]),
    _sweep("Neon · molten", ["#FF1744", "#FF6D00", "#F9FF00", "#FF1744"]),
    _sweep("Neon · cosmic wheel", ["#090026", "#A855F7", "#00D9FF", "#F000FF", "#090026"], stops=[0.0, 0.22, 0.5, 0.78, 1.0], rotation=math.pi / 4),
)


def filter_gradients(group: str) -> tuple[GradientSpec, ...]:
    """Gradientes del grupo indicado (``"Todos"`` devuelve todos)."""
    if group == "Todos":
        return GRADIENTS
    return tuple(g for g in GRADIENTS if g.group == group)


@ft.component
def GradientTile(spec: GradientSpec) -> ft.Control:
    return ft.Container(
        height=200,
        gradient=spec.gradient,
        border_radius=18,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        alignment=ft.Alignment.BOTTOM_CENTER,
        content=ft.Container(
            padding=12,
            bgcolor=ft.Colors.with_opacity(0.75, ft.Colors.BLACK),
            content=ft.Text(
                spec.name,
                color=ft.Colors.WHITE,
                size=14,
                weight=ft.FontWeight.W_600,
                text_align=ft.TextAlign.CENTER,
            ),
        ),
    )


@ft.component
def GradientsGallery() -> ft.Control:
    group, set_group = ft.use_state("Todos")
    return ft.Column(
        spacing=16,
        controls=[
            ft.Row(
                wrap=True,
                controls=[
                    Button(
                        name,
                        variant="default" if name == group else "outline",
                        on_click=lambda _, name=name: set_group(name),
                    )
                    for name in GROUPS
                ],
            ),
            ResponsiveGrid(
                [GradientTile(g, key=g.name) for g in filter_gradients(group)],
                cols={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                spacing=20,
            ),
        ],
    )
