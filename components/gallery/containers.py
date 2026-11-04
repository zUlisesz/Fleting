"""Galería de patrones visuales para ft.Container."""

import flet as ft


def _sample(title: str, control: ft.Control, description: str) -> ft.Container:
    return ft.Container(
        col={"xs": 12, "sm": 6, "md": 4},
        height=210,
        padding=16,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=16,
        content=ft.Column(
            [
                ft.Text(title, size=15, weight=ft.FontWeight.W_600),
                ft.Text(description, size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                ft.Container(expand=True, alignment=ft.Alignment.CENTER, content=control),
            ],
            spacing=8,
        ),
    )


def container_gallery() -> ft.ResponsiveRow:
    """Muestra contenedores con decoración, distribución y contenido diverso."""
    samples = [
        _sample("Superficie elevada", ft.Card(content=ft.Container(padding=18, content=ft.Row([ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET), ft.Column([ft.Text("Balance"), ft.Text("$12,450", size=22, weight=ft.FontWeight.BOLD)])]))), "Tarjeta compacta inspirada en el resumen de finanzas."),
        _sample("Bloque con acento", ft.Container(width=210, padding=14, border=ft.Border(left=ft.BorderSide(4, ft.Colors.TEAL)), bgcolor=ft.Colors.SURFACE_CONTAINER_LOW, content=ft.Text("Movimiento registrado correctamente")), "Borde lateral para resaltar avisos."),
        _sample("Superficie degradada", ft.Container(width=210, height=90, alignment=ft.Alignment.CENTER, border_radius=16, gradient=ft.LinearGradient(colors=[ft.Colors.INDIGO, ft.Colors.PURPLE]), content=ft.Text("Resumen semanal", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)), "Color y texto centrado."),
        _sample("Sombra y elevación", ft.Container(width=160, height=82, alignment=ft.Alignment.CENTER, bgcolor=ft.Colors.WHITE, border_radius=14, shadow=ft.BoxShadow(blur_radius=18, spread_radius=1, color=ft.Colors.BLACK_26, offset=ft.Offset(0, 7)), content=ft.Text("Flotante")), "Sombra suave para separar una superficie."),
        _sample("Indicador de progreso", ft.Container(width=210, padding=14, border_radius=12, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, content=ft.Column([ft.Row([ft.Text("Almacenamiento"), ft.Text("72%")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), ft.ProgressBar(value=0.72, color=ft.Colors.BLUE)])), "Contenido compuesto con barra de avance."),
        _sample("Etiqueta superpuesta", ft.Stack([ft.Container(width=190, height=95, bgcolor=ft.Colors.BLUE_GREY_900, border_radius=14), ft.Container(left=12, top=12, padding=8, bgcolor=ft.Colors.GREEN_400, border_radius=20, content=ft.Text("ACTIVO", size=10, weight=ft.FontWeight.BOLD)), ft.Text("Cajero", left=14, bottom=12, color=ft.Colors.WHITE, size=18, weight=ft.FontWeight.BOLD)]), "Composición de superficie y etiqueta."),
        _sample("Vista de perfil", ft.Container(width=210, padding=12, border_radius=14, bgcolor=ft.Colors.SURFACE_CONTAINER_LOW, content=ft.Row([ft.CircleAvatar(content=ft.Text("MR"), bgcolor=ft.Colors.DEEP_PURPLE, color=ft.Colors.WHITE), ft.Column([ft.Text("María Ruiz", weight=ft.FontWeight.BOLD), ft.Text("Administradora", size=12)])])), "Fila de identidad con avatar."),
        _sample("Contenedor recortado", ft.Container(width=170, height=90, border_radius=18, clip_behavior=ft.ClipBehavior.ANTI_ALIAS, content=ft.Image(src="https://picsum.photos/340/180", fit=ft.BoxFit.COVER)), "Imagen limitada por esquinas redondeadas."),
        _sample("Panel con acción", ft.Container(width=210, padding=14, border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT), border_radius=12, content=ft.Column([ft.Text("Nuevo movimiento", weight=ft.FontWeight.BOLD), ft.Text("Registra un ingreso o gasto", size=12), ft.FilledButton("Agregar", icon=ft.Icons.ADD)])), "Contenedor que agrupa texto y acción."),
    ]
    return ft.ResponsiveRow(controls=samples, spacing=16, run_spacing=16) #type: ignore


def main(page: ft.Page) -> None:
    page.title = "Flet Containers"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    page.add(ft.Text("Containers", size=26, weight=ft.FontWeight.BOLD), container_gallery())


if __name__ == "__main__":
    ft.run(main)
