"""Patrones visuales para ``ft.Container``."""

import flet as ft

from ._layout import sample_grid

W = ft.FontWeight


def _elevated() -> ft.Control:
    return ft.Card(
        content=ft.Container(
            padding=18,
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET),
                    ft.Column(
                        [ft.Text("Balance"), ft.Text("$12,450", size=22, weight=W.BOLD)]
                    ),
                ]
            ),
        )
    )


def _accent() -> ft.Control:
    return ft.Container(
        width=210,
        padding=14,
        border=ft.Border(left=ft.BorderSide(4, ft.Colors.TEAL)),
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Text("Movimiento registrado correctamente"),
    )


def _gradient() -> ft.Control:
    return ft.Container(
        width=210,
        height=90,
        alignment=ft.Alignment.CENTER,
        border_radius=16,
        gradient=ft.LinearGradient(colors=[ft.Colors.INDIGO, ft.Colors.PURPLE]),
        content=ft.Text("Resumen semanal", color=ft.Colors.WHITE, weight=W.BOLD),
    )


def _shadow() -> ft.Control:
    return ft.Container(
        width=160,
        height=82,
        alignment=ft.Alignment.CENTER,
        bgcolor=ft.Colors.WHITE,
        border_radius=14,
        shadow=ft.BoxShadow(
            blur_radius=18,
            spread_radius=1,
            color=ft.Colors.BLACK_26,
            offset=ft.Offset(0, 7),
        ),
        content=ft.Text("Flotante"),
    )


def _progress() -> ft.Control:
    return ft.Container(
        width=210,
        padding=14,
        border_radius=12,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        content=ft.Column(
            [
                ft.Row(
                    [ft.Text("Almacenamiento"), ft.Text("72%")],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.ProgressBar(value=0.72, color=ft.Colors.BLUE),
            ]
        ),
    )


def _overlay() -> ft.Control:
    return ft.Stack(
        [
            ft.Container(width=190, height=95, bgcolor=ft.Colors.BLUE_GREY_900, border_radius=14),
            ft.Container(
                left=12,
                top=12,
                padding=8,
                bgcolor=ft.Colors.GREEN_400,
                border_radius=20,
                content=ft.Text("ACTIVO", size=10, weight=W.BOLD),
            ),
            ft.Text("Cajero", left=14, bottom=12, color=ft.Colors.WHITE, size=18, weight=W.BOLD),
        ]
    )


def _profile() -> ft.Control:
    return ft.Container(
        width=210,
        padding=12,
        border_radius=14,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Row(
            [
                ft.CircleAvatar(
                    content=ft.Text("MR"), bgcolor=ft.Colors.DEEP_PURPLE, color=ft.Colors.WHITE
                ),
                ft.Column(
                    [ft.Text("María Ruiz", weight=W.BOLD), ft.Text("Administradora", size=12)]
                ),
            ]
        ),
    )


def _clipped() -> ft.Control:
    return ft.Container(
        width=170,
        height=90,
        border_radius=18,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        content=ft.Image(src="https://picsum.photos/340/180", fit=ft.BoxFit.COVER),
    )


def _action_panel() -> ft.Control:
    return ft.Container(
        width=210,
        padding=14,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=12,
        content=ft.Column(
            [
                ft.Text("Nuevo movimiento", weight=W.BOLD),
                ft.Text("Registra un ingreso o gasto", size=12),
                ft.FilledButton("Agregar", icon=ft.Icons.ADD),
            ]
        ),
    )


@ft.component
def ContainersGallery() -> ft.Control:
    return sample_grid(
        [
            ("Superficie elevada", "Tarjeta compacta de resumen financiero.", _elevated()),
            ("Bloque con acento", "Borde lateral para resaltar avisos.", _accent()),
            ("Superficie degradada", "Color y texto centrado.", _gradient()),
            ("Sombra y elevación", "Sombra suave para separar una superficie.", _shadow()),
            ("Indicador de progreso", "Contenido compuesto con barra de avance.", _progress()),
            ("Etiqueta superpuesta", "Composición de superficie y etiqueta.", _overlay()),
            ("Vista de perfil", "Fila de identidad con avatar.", _profile()),
            ("Contenedor recortado", "Imagen limitada por esquinas redondeadas.", _clipped()),
            ("Panel con acción", "Contenedor que agrupa texto y acción.", _action_panel()),
        ],
        height=210,
    )
