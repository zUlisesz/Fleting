"""Galería independiente de botones estilizados con Flet."""

import flet as ft


def _button_card(title: str, button: ft.Control) -> ft.Container:
    """Presenta un botón dentro de una tarjeta adaptable."""

    return ft.Container(
        col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
        height=150,
        padding=20,
        border=ft.Border.all(1, "#E2E8F0"),
        border_radius=18,
        bgcolor="#FFFFFF",
        content=ft.Column(
            controls=[
                ft.Text(title, size=12, color="#64748B", weight=ft.FontWeight.W_600),
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                    content=button,
                ),
            ],
            spacing=8,
        ),
    )


def _styled_button(
    text: str,
    *,
    icon: ft.IconData | None = None,
    color: str = "#FFFFFF",
    bgcolor: str = "#2563EB",
    hover_bgcolor: str | None = None,
    radius: float = 10,
    elevation: float = 0,
    border_color: str | None = None,
    border_width: float = 1,
    padding: int = 18,
    width: float | None = None,
    height: float = 46,
    shape: ft.OutlinedBorder | None = None,
    disabled: bool = False,
) -> ft.Button:
    """Construye un botón actual y configura también sus estados interactivos."""

    background = hover_bgcolor or bgcolor
    return ft.Button(
        content=text,
        icon=icon,
        disabled=disabled,
        width=width,
        height=height,
        style=ft.ButtonStyle(
            color={
                ft.ControlState.DEFAULT: color,
                ft.ControlState.DISABLED: "#94A3B8",
            },
            bgcolor={
                ft.ControlState.DEFAULT: bgcolor,
                ft.ControlState.HOVERED: background,
                ft.ControlState.PRESSED: background,
                ft.ControlState.DISABLED: "#E2E8F0",
            },
            elevation={
                ft.ControlState.DEFAULT: elevation,
                ft.ControlState.HOVERED: elevation + 4,
                ft.ControlState.PRESSED: 0,
            },
            padding=padding,
            side=(
                ft.BorderSide(border_width, border_color)
                if border_color is not None
                else None
            ),
            shape=shape or ft.RoundedRectangleBorder(radius=radius),
            animation_duration=180,
            mouse_cursor=ft.MouseCursor.CLICK,
            text_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_600),
        ),
    )


def styled_button_gallery() -> ft.ResponsiveRow:
    """Devuelve una colección adaptable de botones con estilos distintos."""

    examples = [
        (
            "Primario",
            _styled_button(
                "Continuar", icon=ft.Icons.ARROW_FORWARD, hover_bgcolor="#1D4ED8"
            ),
        ),
        (
            "Secundario",
            _styled_button(
                "Ver detalles",
                icon=ft.Icons.VISIBILITY_OUTLINED,
                color="#334155",
                bgcolor="#F1F5F9",
                hover_bgcolor="#E2E8F0",
            ),
        ),
        (
            "Contorno",
            _styled_button(
                "Editar",
                icon=ft.Icons.EDIT_OUTLINED,
                color="#2563EB",
                bgcolor="#FFFFFF",
                hover_bgcolor="#EFF6FF",
                border_color="#2563EB",
            ),
        ),
        (
            "Píldora",
            _styled_button(
                "Explorar",
                icon=ft.Icons.EXPLORE_OUTLINED,
                bgcolor="#7C3AED",
                hover_bgcolor="#6D28D9",
                shape=ft.StadiumBorder(),
                padding=22,
            ),
        ),
        (
            "Éxito",
            _styled_button(
                "Completado",
                icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                bgcolor="#16A34A",
                hover_bgcolor="#15803D",
            ),
        ),
        (
            "Alerta",
            _styled_button(
                "Eliminar",
                icon=ft.Icons.DELETE_OUTLINE,
                bgcolor="#DC2626",
                hover_bgcolor="#B91C1C",
            ),
        ),
        (
            "Suave",
            _styled_button(
                "Favorito",
                icon=ft.Icons.FAVORITE_BORDER,
                color="#BE185D",
                bgcolor="#FCE7F3",
                hover_bgcolor="#FBCFE8",
                radius=14,
            ),
        ),
        (
            "Oscuro",
            _styled_button(
                "Abrir consola",
                icon=ft.Icons.TERMINAL,
                bgcolor="#0F172A",
                hover_bgcolor="#1E293B",
                radius=8,
                elevation=3,
            ),
        ),
        (
            "Neón",
            _styled_button(
                "Activar",
                icon=ft.Icons.BOLT,
                color="#0F172A",
                bgcolor="#67E8F9",
                hover_bgcolor="#22D3EE",
                border_color="#0891B2",
                border_width=2,
                elevation=8,
                radius=14,
            ),
        ),
        (
            "Cálido",
            _styled_button(
                "Descubrir",
                icon=ft.Icons.WB_SUNNY_OUTLINED,
                color="#431407",
                bgcolor="#FDBA74",
                hover_bgcolor="#FB923C",
                radius=16,
            ),
        ),
        (
            "Esquinas biseladas",
            _styled_button(
                "Construir",
                icon=ft.Icons.HANDYMAN_OUTLINED,
                bgcolor="#4F46E5",
                hover_bgcolor="#4338CA",
                shape=ft.BeveledRectangleBorder(radius=10),
            ),
        ),
        (
            "Esquinas continuas",
            _styled_button(
                "Crear nuevo",
                icon=ft.Icons.ADD,
                color="#3F3F46",
                bgcolor="#FAFAFA",
                hover_bgcolor="#F4F4F5",
                border_color="#A1A1AA",
                shape=ft.ContinuousRectangleBorder(radius=28),
            ),
        ),
        (
            "Compacto",
            _styled_button(
                "Filtrar",
                icon=ft.Icons.FILTER_ALT_OUTLINED,
                color="#0F766E",
                bgcolor="#CCFBF1",
                hover_bgcolor="#99F6E4",
                height=36,
                padding=12,
                radius=8,
            ),
        ),
        (
            "Acción amplia",
            _styled_button(
                "Guardar cambios",
                icon=ft.Icons.SAVE_OUTLINED,
                bgcolor="#0284C7",
                hover_bgcolor="#0369A1",
                width=210,
                height=52,
                radius=12,
                elevation=2,
            ),
        ),
        (
            "Monocromático",
            _styled_button(
                "Compartir",
                icon=ft.Icons.SHARE_OUTLINED,
                color="#18181B",
                bgcolor="#FFFFFF",
                hover_bgcolor="#F4F4F5",
                border_color="#18181B",
                border_width=2,
                radius=0,
            ),
        ),
        (
            "Deshabilitado",
            _styled_button(
                "No disponible",
                icon=ft.Icons.LOCK_OUTLINE,
                color="#64748B",
                bgcolor="#E2E8F0",
                disabled=True,
            ),
        ),
    ]

    return ft.ResponsiveRow(
        controls=[_button_card(title, button) for title, button in examples],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=18,
        run_spacing=18,
    )


def main(page: ft.Page) -> None:
    """Abre la galería como una aplicación independiente."""

    page.title = "Galería de botones estilizados"
    page.bgcolor = "#F8FAFC"
    page.padding = 24
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(
        ft.Text(
            "Botones estilizados",
            size=30,
            weight=ft.FontWeight.BOLD,
            color="#0F172A",
        ),
        ft.Text(
            "Variantes visuales, estados y formas construidas con Flet.",
            size=15,
            color="#64748B",
        ),
        styled_button_gallery(),
    )


if __name__ == "__main__":
    ft.run(main)
