"""Galería variada de tarjetas para interfaces Flet."""

import flet as ft


def _frame(title: str, content: ft.Control) -> ft.Container:
    return ft.Container(
        col={"xs": 12, "sm": 6, "md": 4},
        padding=12,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=16,
        content=ft.Column([ft.Text(title, size=12, color=ft.Colors.ON_SURFACE_VARIANT), content], spacing=10),
    )


def card_gallery() -> ft.ResponsiveRow:
    """Presenta tarjetas de perfil, métrica, producto, aviso, actividad y resumen."""
    cards = [
        _frame("PERFIL", ft.Card(content=ft.Container(padding=16, content=ft.Column([ft.CircleAvatar(radius=34, foreground_image_src="https://i.pravatar.cc/136?img=47"), ft.Text("Sofía Martínez", size=17, weight=ft.FontWeight.BOLD), ft.Text("Diseñadora de producto", size=12), ft.Row([ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, size=16), ft.Text("Ciudad de México", size=12)])], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8)))),
        _frame("MÉTRICA", ft.Container(padding=18, border_radius=14, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, content=ft.Column([ft.Row([ft.Text("Ingresos"), ft.Icon(ft.Icons.TRENDING_UP, color=ft.Colors.GREEN)] , alignment=ft.MainAxisAlignment.SPACE_BETWEEN), ft.Text("$24,580", size=28, weight=ft.FontWeight.BOLD), ft.Text("▲ 12.8% respecto al mes pasado", size=11, color=ft.Colors.GREEN_700)]))),
        _frame("PRODUCTO", ft.Card(clip_behavior=ft.ClipBehavior.ANTI_ALIAS, content=ft.Column([ft.Image(src="https://picsum.photos/600/300?food", height=120, fit=ft.BoxFit.COVER), ft.Container(padding=14, content=ft.Column([ft.Text("Ensalada de temporada", size=16, weight=ft.FontWeight.BOLD), ft.Text("Fresca, ligera y lista en 15 minutos", size=12), ft.Row([ft.Text("$145", size=18, weight=ft.FontWeight.BOLD), ft.IconButton(ft.Icons.FAVORITE_BORDER)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)]))]))),
        _frame("ESTADO", ft.Container(padding=16, border_radius=14, bgcolor=ft.Colors.GREEN_50, content=ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_700, size=30), ft.Column([ft.Text("Pago recibido", weight=ft.FontWeight.BOLD), ft.Text("Pedido #2048 · hace 2 min", size=11)])]))),
        _frame("ACTIVIDAD", ft.Card(content=ft.Container(padding=16, content=ft.Column([ft.Text("Actividad reciente", weight=ft.FontWeight.BOLD), ft.ListTile(leading=ft.Icon(ft.Icons.FILE_DOWNLOAD_OUTLINED), title=ft.Text("Reporte descargado"), subtitle=ft.Text("Hoy · 10:42")), ft.ListTile(leading=ft.Icon(ft.Icons.PERSON_ADD_ALT_1), title=ft.Text("Nuevo integrante"), subtitle=ft.Text("Ayer · 16:18"))], spacing=4)))),
        _frame("ACCIÓN", ft.Container(padding=18, border_radius=14, gradient=ft.LinearGradient(colors=[ft.Colors.INDIGO, ft.Colors.DEEP_PURPLE]), content=ft.Column([ft.Icon(ft.Icons.ROCKET_LAUNCH, color=ft.Colors.WHITE, size=30), ft.Text("Tu espacio está listo", size=17, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD), ft.Text("Invita a tu equipo y empieza a colaborar.", color=ft.Colors.WHITE, size=12), ft.OutlinedButton("Invitar equipo", icon=ft.Icons.ARROW_FORWARD, style=ft.ButtonStyle(color=ft.Colors.WHITE))], spacing=10))),
        _frame("PROGRESO", ft.Container(padding=16, border_radius=14, border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT), content=ft.Column([ft.Row([ft.Text("Configuración", weight=ft.FontWeight.BOLD), ft.Text("3 de 5")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), ft.ProgressBar(value=0.6), ft.Text("Completa tu perfil para aprovechar todas las funciones.", size=11)]))),
        _frame("ELEMENTO DE LISTA", ft.Card(content=ft.ListTile(leading=ft.Icon(ft.Icons.RECEIPT_LONG), title=ft.Text("Compra de materiales"), subtitle=ft.Text("Oficina · 3 nov 2026"), trailing=ft.Text("−$820", color=ft.Colors.RED_700)))),
        _frame("PRODUCTO DESTACADO", ft.Container(padding=16, border_radius=14, bgcolor=ft.Colors.AMBER_50, content=ft.Row([ft.Container(width=58, height=58, alignment=ft.Alignment.CENTER, border_radius=12, bgcolor=ft.Colors.AMBER_100, content=ft.Icon(ft.Icons.COFFEE, color=ft.Colors.BROWN)), ft.Column([ft.Text("Café de origen", weight=ft.FontWeight.BOLD), ft.Text("Tueste medio · 340 g", size=11), ft.Text("★★★★★  4.9", color=ft.Colors.AMBER_900, size=12)])]))),
    ]
    return ft.ResponsiveRow(controls= cards, spacing=16, run_spacing=16) #type: ignore


def main(page: ft.Page) -> None:
    page.title = "Flet Cards"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    page.add(ft.Text("Cards", size=26, weight=ft.FontWeight.BOLD), card_gallery())


if __name__ == "__main__":
    ft.run(main)
