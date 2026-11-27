"""Panel derecho: detalle de la receta seleccionada."""

from collections.abc import Callable

import flet as ft

from domain import IngredientLine, Instruction, RecipeDetail

from . import theme
from .widgets import EmptyHint, SectionCard


@ft.component
def NoSelection(*, on_create: Callable[[], None]) -> ft.Control:
    return ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=14,
            controls=[
                ft.Icon(ft.Icons.RESTAURANT_MENU, size=64, color=ft.Colors.GREY_300),
                ft.Text(
                    "Selecciona o crea una receta",
                    size=18,
                    weight=ft.FontWeight.W_500,
                    color=theme.FAINT,
                ),
                ft.FilledButton(
                    content=ft.Text("Crear primera receta"),
                    icon=ft.Icons.ADD,
                    bgcolor=theme.ACCENT,
                    on_click=lambda _: on_create(),
                ),
            ],
        ),
    )


@ft.component
def ErrorMessage(message: str, *, on_retry: Callable[[], None]) -> ft.Control:
    """Pantalla de error con opción de reintentar (p. ej. MySQL no disponible)."""
    return ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=14,
            controls=[
                ft.Icon(ft.Icons.ERROR_OUTLINE, size=48, color=theme.DANGER),
                ft.Text(message, color=theme.DANGER, text_align=ft.TextAlign.CENTER),
                ft.FilledButton(
                    content=ft.Text("Reintentar"),
                    icon=ft.Icons.REFRESH,
                    bgcolor=theme.ACCENT,
                    on_click=lambda _: on_retry(),
                ),
            ],
        ),
    )


@ft.component
def RecipeHeader(
    detail: RecipeDetail, *, on_edit: Callable[[], None], on_delete: Callable[[], None]
) -> ft.Control:
    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row(
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                controls=[
                    ft.Container(
                        padding=10,
                        bgcolor=ft.Colors.TEAL_100,
                        border_radius=12,
                        content=ft.Icon(ft.Icons.DINNER_DINING, color=ft.Colors.TEAL_800, size=28),
                    ),
                    ft.Column(
                        spacing=2,
                        expand=True,
                        controls=[
                            ft.Text(
                                detail.title,
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                color=theme.TEXT_STRONG,
                            ),
                            ft.Text(f"ID: {detail.id[:8]}...", size=11, color=ft.Colors.GREY_400),
                        ],
                    ),
                ],
            ),
            ft.Row(
                spacing=6,
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.EDIT_OUTLINED,
                        tooltip="Editar título",
                        icon_color=ft.Colors.GREY_700,
                        on_click=lambda _: on_edit(),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                        tooltip="Eliminar receta",
                        icon_color=ft.Colors.RED_500,
                        on_click=lambda _: on_delete(),
                    ),
                ],
            ),
        ],
    )


def _row_card(content: ft.Control, padding: ft.PaddingValue) -> ft.Container:
    return ft.Container(
        padding=padding,
        border_radius=8,
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, theme.BORDER),
        content=content,
    )


@ft.component
def IngredientRow(line: IngredientLine, *, on_remove: Callable[[IngredientLine], None]) -> ft.Control:
    quantity = line.quantity
    return _row_card(
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    spacing=8,
                    expand=True,
                    controls=[
                        ft.Icon(ft.Icons.CIRCLE, size=8, color=theme.ACCENT),
                        ft.Text(line.name, weight=ft.FontWeight.W_600, size=13, color=theme.TEXT),
                        ft.Text(f"— {quantity}" if quantity else "", size=13, color=theme.MUTED),
                    ],
                ),
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_size=16,
                    tooltip="Quitar ingrediente",
                    icon_color=theme.FAINT,
                    on_click=lambda _: on_remove(line),
                ),
            ],
        ),
        ft.Padding(left=12, top=8, right=8, bottom=8),
    )


@ft.component
def StepRow(step: Instruction, *, on_delete: Callable[[Instruction], None]) -> ft.Control:
    return _row_card(
        ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    expand=True,
                    controls=[
                        ft.Container(
                            width=26,
                            height=26,
                            border_radius=13,
                            bgcolor=theme.ACCENT,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Text(
                                str(step.step_number),
                                color=ft.Colors.WHITE,
                                size=12,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ),
                        ft.Text(step.instruction, size=13, color=theme.TEXT, selectable=True, expand=True),
                    ],
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                    icon_size=18,
                    tooltip="Eliminar paso",
                    icon_color=theme.FAINT,
                    on_click=lambda _: on_delete(step),
                ),
            ],
        ),
        12,
    )


@ft.component
def RecipeDetailView(
    detail: RecipeDetail,
    *,
    on_edit: Callable[[], None],
    on_delete: Callable[[], None],
    on_add_ingredient: Callable[[], None],
    on_remove_ingredient: Callable[[IngredientLine], None],
    on_add_step: Callable[[], None],
    on_delete_step: Callable[[Instruction], None],
) -> ft.Control:
    ingredients = [
        IngredientRow(line, on_remove=on_remove_ingredient, key=line.link_id)
        for line in detail.ingredients
    ] or [EmptyHint("No has agregado ingredientes aún.")]
    steps = [
        StepRow(step, on_delete=on_delete_step, key=step.id) for step in detail.instructions
    ] or [EmptyHint("No has agregado pasos o instrucciones aún.")]

    return ft.ListView(
        expand=True,
        spacing=16,
        controls=[
            RecipeHeader(detail, on_edit=on_edit, on_delete=on_delete),
            ft.Divider(height=1, color=ft.Colors.GREY_300),
            SectionCard(
                "Ingredientes",
                icon=ft.Icons.ECO_ROUNDED,
                icon_color=ft.Colors.GREEN_700,
                count=len(detail.ingredients),
                badge_bgcolor=ft.Colors.GREEN_50,
                badge_color=ft.Colors.GREEN_800,
                action_label="Agregar",
                on_action=on_add_ingredient,
                spacing=6,
                children=ingredients,
            ),
            SectionCard(
                "Preparación y pasos",
                icon=ft.Icons.FORMAT_LIST_NUMBERED_ROUNDED,
                icon_color=theme.ACCENT_DARK,
                count=len(detail.instructions),
                badge_bgcolor=theme.ACCENT_SOFT,
                badge_color=ft.Colors.TEAL_800,
                action_label="Agregar paso",
                on_action=on_add_step,
                spacing=8,
                children=steps,
            ),
        ],
    )
