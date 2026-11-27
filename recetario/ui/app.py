"""Componente raíz: estado de la pantalla y coordinación con el servicio."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

import flet as ft

from database import StorageError
from domain import IngredientLine, Instruction, Recipe, RecipeDetail
from services import RecipeService

from .detail import ErrorMessage, NoSelection, RecipeDetailView
from .dialogs import (
    ConfirmDeleteDialog,
    IngredientDialog,
    RecipeTitleDialog,
    StepDialog,
)
from .sidebar import Sidebar
from .widgets import Notice, Toast

T = TypeVar("T")
EXPECTED_ERRORS = (ValueError, StorageError)


# Acciones pendientes: qué diálogo está abierto.
@dataclass(frozen=True)
class NewRecipe:
    pass


@dataclass(frozen=True)
class EditRecipe:
    recipe: Recipe


@dataclass(frozen=True)
class DeleteRecipe:
    recipe: Recipe


@dataclass(frozen=True)
class AddIngredient:
    recipe_id: str


@dataclass(frozen=True)
class AddStep:
    recipe_id: str
    next_number: int


def load(call: Callable[[], T], fallback: T) -> tuple[T, str | None]:
    """Resultado de ``call`` o ``(fallback, mensaje)`` si falla de forma esperada."""
    try:
        return call(), None
    except EXPECTED_ERRORS as error:
        return fallback, str(error)


def filter_recipes(recipes: list[Recipe], query: str) -> list[Recipe]:
    """Recetas cuyo título contiene ``query`` (sin distinguir mayúsculas)."""
    term = query.strip().casefold()
    return [r for r in recipes if term in r.title.casefold()]


def resolve_selection(recipes: list[Recipe], selected_id: str | None) -> str | None:
    """La receta elegida si sigue existiendo; si no, la primera (o ninguna)."""
    if any(r.id == selected_id for r in recipes):
        return selected_id
    return recipes[0].id if recipes else None


@ft.component
def App(service: RecipeService) -> ft.Control:
    revision, set_revision = ft.use_state(0)  # sube tras cambiar la base de datos
    selected_id, set_selected_id = ft.use_state(None)
    query, set_query = ft.use_state("")
    action, set_action = ft.use_state(None)  # acción con diálogo abierto, o None
    notice, set_notice = ft.use_state(None)

    recipes, recipes_error = ft.use_memo(
        lambda: load(service.get_all_recipes, []), [service, revision]
    )
    current_id = resolve_selection(recipes, selected_id)
    detail, detail_error = ft.use_memo(
        lambda: load(lambda: service.get_recipe_detail(current_id), None) if current_id else (None, None),
        [service, current_id, revision],
    )

    def refresh() -> None:
        set_revision(lambda r: r + 1)

    def notify(text: str, *, error: bool = False) -> None:
        set_notice(Notice(text, error))

    def close() -> None:
        set_action(None)

    def perform(work: Callable[[], object], success: str) -> None:
        """Acción directa (sin formulario): avisa del resultado y recarga."""
        try:
            work()
        except EXPECTED_ERRORS as error:
            notify(str(error), error=True)
            return
        refresh()
        notify(success)

    # Los formularios dejan que las excepciones lleguen al diálogo para mostrarlas.

    def create_recipe(title: str) -> None:
        recipe = service.create_recipe(title)
        set_selected_id(recipe.id)
        close()
        refresh()
        notify(f"Receta «{recipe.title}» creada.")

    def rename_recipe(recipe: Recipe, title: str) -> None:
        service.update_recipe_title(recipe.id, title)
        close()
        refresh()
        notify("Título de receta actualizado.")

    def add_ingredient(recipe_id: str, name: str, amount: str, unit: str) -> None:
        service.add_ingredient_to_recipe(recipe_id, name, amount=amount, unit=unit)
        close()
        refresh()
        notify(f"Ingrediente «{name.strip()}» agregado.")

    def add_step(recipe_id: str, number: int, text: str) -> None:
        service.add_step(recipe_id, number, text)
        close()
        refresh()
        notify("Paso añadido.")

    def delete_recipe(recipe: Recipe) -> None:
        close()
        perform(lambda: service.delete_recipe(recipe.id), f"Receta «{recipe.title}» eliminada.")

    def remove_ingredient(line: IngredientLine) -> None:
        perform(
            lambda: service.remove_ingredient_from_recipe(line.link_id),
            f"Ingrediente «{line.name}» removido de la receta.",
        )

    def delete_step(step: Instruction) -> None:
        perform(lambda: service.delete_step(step.id), f"Paso #{step.step_number} eliminado.")

    def open_new_recipe() -> None:
        set_action(NewRecipe())

    # Panel derecho
    if recipes_error:
        body: ft.Control = ErrorMessage(
            f"No se pudo cargar el recetario: {recipes_error}", on_retry=refresh
        )
    elif detail_error:
        body = ErrorMessage(f"No se pudo cargar la receta: {detail_error}", on_retry=refresh)
    elif detail is None:
        body = NoSelection(on_create=open_new_recipe)
    else:
        body = RecipeDetailView(
            detail,
            on_edit=lambda: set_action(EditRecipe(Recipe(id=detail.id, title=detail.title))),
            on_delete=lambda: set_action(DeleteRecipe(Recipe(id=detail.id, title=detail.title))),
            on_add_ingredient=lambda: set_action(AddIngredient(detail.id)),
            on_remove_ingredient=remove_ingredient,
            on_add_step=lambda: set_action(AddStep(detail.id, detail.next_step_number)),
            on_delete_step=delete_step,
        )

    # Diálogo abierto: se monta solo mientras hay una acción pendiente.
    overlay: ft.Control | None = None
    if isinstance(action, NewRecipe):
        overlay = RecipeTitleDialog(
            "Nueva receta",
            confirm_label="Guardar",
            hint="Escribe el nombre de tu platillo:",
            on_submit=create_recipe,
            on_close=close,
            key="new-recipe",
        )
    elif isinstance(action, EditRecipe):
        overlay = RecipeTitleDialog(
            "Editar receta",
            confirm_label="Actualizar",
            initial=action.recipe.title,
            on_submit=lambda title: rename_recipe(action.recipe, title),
            on_close=close,
            key=f"edit-{action.recipe.id}",
        )
    elif isinstance(action, DeleteRecipe):
        overlay = ConfirmDeleteDialog(
            "Eliminar receta",
            f"¿Estás seguro de que deseas eliminar la receta «{action.recipe.title}»? "
            "Esta acción no se puede deshacer.",
            on_confirm=lambda: delete_recipe(action.recipe),
            on_close=close,
            key=f"delete-{action.recipe.id}",
        )
    elif isinstance(action, AddIngredient):
        overlay = IngredientDialog(
            on_submit=lambda name, amount, unit: add_ingredient(
                action.recipe_id, name, amount, unit
            ),
            on_close=close,
            key=f"ingredient-{action.recipe_id}",
        )
    elif isinstance(action, AddStep):
        overlay = StepDialog(
            action.next_number,
            on_submit=lambda number, text: add_step(action.recipe_id, number, text),
            on_close=close,
            key=f"step-{action.recipe_id}",
        )

    return ft.Row(
        spacing=0,
        expand=True,
        controls=[
            Sidebar(
                filter_recipes(recipes, query),
                selected_id=current_id,
                query=query,
                on_query=set_query,
                on_select=set_selected_id,
                on_new=open_new_recipe,
            ),
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.GREY_100,
                padding=ft.Padding.symmetric(horizontal=28, vertical=20),
                content=body,
            ),
            # Diálogo y aviso: visibles solo mientras estén montados.
            *([overlay] if overlay else []),
            *([Toast(notice, on_dismiss=lambda: set_notice(None), key=f"toast-{id(notice)}")] if notice else []),
        ],
    )
