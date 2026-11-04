"""Galería navegable de los iconos disponibles en ``ft.Icons``."""

import flet as ft

PAGE_SIZE = 120


def _icon_tile(icon: ft.Icons) -> ft.Container:
    """Muestra el glifo y los datos necesarios para reutilizarlo."""
    return ft.Container(
        col={"xs": 6, "sm": 4, "md": 3, "lg": 2},
        height=116,
        padding=10,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        bgcolor= ft.Colors.TRANSPARENT,
        border_radius=12,
        content=ft.Column(
            [
                ft.Icon(icon, size=26, color=ft.Colors.TEAL_ACCENT),
                ft.Text(icon.name, size=10, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Text(f"ft.Icons.{icon.name} · {icon.value} · {icon.name.lower()}", size=8, color=ft.Colors.ON_SURFACE_VARIANT, text_align=ft.TextAlign.CENTER, selectable=True),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
        ),
    )


def icon_gallery() -> ft.Column:
    """Devuelve una galería con filtro por nombre y navegación paginada."""
    icons = list(ft.Icons)
    query = ft.TextField(label="Buscar icono", hint_text="ADD, home, arrow…", prefix_icon=ft.Icons.SEARCH, expand=True)
    info = ft.Text()
    grid = ft.ResponsiveRow(spacing=10, run_spacing=10)
    previous = ft.OutlinedButton("Anterior", icon=ft.Icons.CHEVRON_LEFT)
    next_page = ft.OutlinedButton("Siguiente", icon=ft.Icons.CHEVRON_RIGHT)
    state = {"page": 0, "matches": icons, "mounted": False}

    def render(_: ft.ControlEvent | None = None) -> None:
        term = (query.value or "").strip().casefold()
        state["matches"] = [icon for icon in icons if term in icon.name.casefold()]
        pages = max(1, (len(state["matches"]) + PAGE_SIZE - 1) // PAGE_SIZE)
        state["page"] = min(state["page"], pages - 1)
        start = state["page"] * PAGE_SIZE
        grid.controls = [_icon_tile(icon) for icon in state["matches"][start : start + PAGE_SIZE]]
        info.value = f"{len(state['matches']):,} iconos · página {state['page'] + 1} de {pages} · ft.Icons.NOMBRE"
        previous.disabled = state["page"] == 0
        next_page.disabled = state["page"] >= pages - 1
        if state["mounted"]:
            grid.update()
            info.update()
            previous.update()
            next_page.update()

    def move(delta: int):
        def handler(_: ft.ControlEvent) -> None:
            state["page"] += delta
            render()
        return handler

    query.on_change = render
    previous.on_click = move(-1)
    next_page.on_click = move(1)
    render()
    state["mounted"] = True
    return ft.Column([ft.Text("ft.Icons", size=24, weight=ft.FontWeight.BOLD), ft.Text(f"{len(icons):,} miembros · nombre, valor entero, acceso Python y muestra visual."), ft.Row([query]), info, ft.Row([previous, next_page], alignment=ft.MainAxisAlignment.CENTER), grid], spacing=12, expand=True)


def main(page: ft.Page) -> None:
    page.title = "Flet Icons"
    page.padding = 16
    page.scroll = ft.ScrollMode.AUTO
    page.add(icon_gallery())


if __name__ == "__main__":
    ft.run(main)
