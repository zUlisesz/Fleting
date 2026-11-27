"""Demostración de ``TextInput``, ``SearchInput`` y ``Surface``."""

import flet as ft

from ..atoms import SearchInput, Surface, TextInput

COMPONENTS = (
    "Button",
    "IconButton",
    "TextInput",
    "SearchInput",
    "Surface",
    "Shimmer",
    "ResponsiveGrid",
)


@ft.component
def InputsGallery() -> ft.Control:
    query, set_query = ft.use_state("")
    name, set_name = ft.use_state("")
    term = query.strip().casefold()
    matches = [c for c in COMPONENTS if term in c.casefold()]

    return ft.Column(
        spacing=20,
        controls=[
            Surface(
                ft.Column(
                    spacing=12,
                    controls=[
                        ft.Text("SearchInput", weight=ft.FontWeight.W_600),
                        SearchInput(
                            value=query,
                            hint_text="Buscar componentes",
                            on_change=lambda e: set_query(e.control.value),
                        ),
                        ft.Text(
                            ", ".join(matches) or "Sin resultados",
                            color=ft.Colors.ON_SURFACE_VARIANT,
                        ),
                    ],
                )
            ),
            Surface(
                ft.Column(
                    spacing=12,
                    controls=[
                        ft.Text("TextInput", weight=ft.FontWeight.W_600),
                        TextInput(
                            "Nombre",
                            value=name,
                            hint_text="Ada Lovelace",
                            on_change=lambda e: set_name(e.control.value),
                        ),
                        TextInput(
                            "Contraseña",
                            password=True,
                            can_reveal_password=True,
                        ),
                        ft.Text(
                            f"Hola, {name}" if name else "Escribe tu nombre",
                            color=ft.Colors.ON_SURFACE_VARIANT,
                        ),
                    ],
                )
            ),
        ],
    )
