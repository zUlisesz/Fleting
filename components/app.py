"""Aplicación del catálogo: barra lateral + galería seleccionada."""

import flet as ft

from .gallery import SECTIONS
from .theme import COLORS


@ft.component
def Sidebar(selected: int, on_select) -> ft.Control:
    return ft.NavigationRail(
        selected_index=selected,
        label_type=ft.NavigationRailLabelType.ALL,
        scrollable=True,
        min_width=96,
        bgcolor=COLORS.surface,
        destinations=[
            ft.NavigationRailDestination(icon=s.icon, label=s.title) for s in SECTIONS
        ],
        on_change=lambda e: on_select(e.control.selected_index),
    )


@ft.component
def App() -> ft.Control:
    selected, set_selected = ft.use_state(0)
    section = SECTIONS[selected]

    return ft.Row(
        expand=True,
        spacing=0,
        controls=[
            Sidebar(selected, set_selected),
            ft.VerticalDivider(width=1, color=COLORS.border),
            ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                spacing=8,
                controls=[
                    ft.Container(
                        padding=ft.Padding.only(left=32, right=32, top=28, bottom=8),
                        content=ft.Column(
                            spacing=4,
                            controls=[
                                ft.Text(
                                    section.title,
                                    size=28,
                                    weight=ft.FontWeight.W_700,
                                    color=COLORS.text,
                                ),
                                ft.Text(section.description, color=COLORS.muted),
                            ],
                        ),
                    ),
                    ft.Container(
                        padding=ft.Padding.only(left=32, right=32, bottom=32),
                        content=section.view(key=section.key),
                    ),
                ],
            ),
        ],
    )
