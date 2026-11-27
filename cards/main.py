"""Tarjetas de perfil con Flet 1.0: UI declarativa con componentes y hooks."""

import flet as ft

try:
    from .model import User, generate_users
except ImportError:  # Permite ejecutar: python main.py desde esta carpeta.
    from model import User, generate_users

MIN_USUARIOS = 1
MAX_USUARIOS = 12
USUARIOS_INICIALES = 5


@ft.component
def UserCard(user: User) -> ft.Control:
    """Tarjeta de un perfil; se vuelve a renderizar solo si cambia ``user``."""
    return ft.Container(
        padding=20,
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        border_radius=24,
        content=ft.Column(
            spacing=16,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Image(
                    src=user["avatar"],
                    width=100,
                    height=140,
                    fit=ft.BoxFit.COVER,
                    border_radius=10,
                ),
                ft.Text(
                    user["name"],
                    weight=ft.FontWeight.W_600,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(user["phone"], size=12, text_align=ft.TextAlign.CENTER),
                ft.Text(
                    user["address"],
                    size=11,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        ),
    )


@ft.component
def Toolbar(cantidad: int, on_cantidad, on_regenerar) -> ft.Control:
    """Controles: cuántos perfiles mostrar y botón para regenerarlos."""
    return ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Text(f"Perfiles: {cantidad}"),
            ft.Slider(
                min=MIN_USUARIOS,
                max=MAX_USUARIOS,
                divisions=MAX_USUARIOS - MIN_USUARIOS,
                value=cantidad,
                width=240,
                on_change=lambda e: on_cantidad(int(e.control.value)),
            ),
            ft.IconButton(
                icon=ft.Icons.REFRESH,
                tooltip="Regenerar perfiles",
                on_click=lambda _: on_regenerar(),
            ),
        ],
    )


@ft.component
def App() -> ft.Control:
    cantidad, set_cantidad = ft.use_state(USUARIOS_INICIALES)
    version, set_version = ft.use_state(0)  # cambia al regenerar

    # Solo se recalcula cuando cambia la cantidad o se pide regenerar.
    usuarios = ft.use_memo(lambda: generate_users(cantidad), [cantidad, version])

    return ft.SafeArea(
        content=ft.Column(
            spacing=24,
            controls=[
                Toolbar(
                    cantidad,
                    on_cantidad=set_cantidad,
                    on_regenerar=lambda: set_version(lambda v: v + 1),
                ),
                ft.ResponsiveRow(
                    columns=12,
                    spacing=16,
                    run_spacing=16,
                    # ``col`` va en un contenedor propio: ResponsiveRow lo lee de sus hijos
                    # directos y un componente no lo expone.
                    controls=[
                        ft.Container(col={"xs": 12, "sm": 6, "lg": 3}, content=UserCard(u))
                        for u in usuarios
                    ],
                ),
            ],
        )
    )


def main(page: ft.Page) -> None:
    page.title = "Cards · Perfiles de usuario"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 1200
    page.window.alignment = ft.Alignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.render(App)


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
