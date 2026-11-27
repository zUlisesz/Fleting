"""Diálogos de captura y confirmación.

Cada diálogo es un componente que se muestra mientras está montado
(``ft.use_dialog``) y se cierra al desmontarse; el padre decide cuándo montarlo.
Los formularios llaman a ``on_submit``: si lanza ``ValueError`` o ``StorageError``,
el mensaje aparece en el diálogo y este sigue abierto.
"""

from collections.abc import Callable

import flet as ft

from database import StorageError

from . import theme

FORM_ERRORS = (ValueError, StorageError)


def _alert(
    title: ft.Control,
    body: ft.Control,
    *,
    confirm_label: str,
    confirm_color: str,
    on_confirm: Callable[[], None],
    on_close: Callable[[], None],
) -> ft.AlertDialog:
    return ft.AlertDialog(
        modal=True,
        title=title,
        content=body,
        actions=[
            ft.TextButton("Cancelar", on_click=lambda _: on_close()),
            ft.FilledButton(
                content=ft.Text(confirm_label),
                bgcolor=confirm_color,
                on_click=lambda _: on_confirm(),
            ),
        ],
    )


def _form_body(width: int, controls: list[ft.Control], error: str | None) -> ft.Control:
    return ft.Container(
        width=width,
        content=ft.Column(
            spacing=12,
            tight=True,
            controls=[
                *controls,
                ft.Text(error or "", color=theme.DANGER, size=12, visible=bool(error)),
            ],
        ),
    )


def _title(text: str, color: str | None = None) -> ft.Text:
    return ft.Text(text, weight=ft.FontWeight.BOLD, color=color)


def _submit_with_errors(submit: Callable[[], None], set_error: Callable[[str | None], None]) -> None:
    try:
        submit()
    except FORM_ERRORS as error:
        set_error(str(error))


@ft.component
def RecipeTitleDialog(
    title: str,
    *,
    confirm_label: str,
    on_submit: Callable[[str], None],
    on_close: Callable[[], None],
    initial: str = "",
    hint: str | None = None,
) -> ft.Control:
    text, set_text = ft.use_state(initial)
    error, set_error = ft.use_state(None)

    def confirm() -> None:
        _submit_with_errors(lambda: on_submit(text), set_error)

    controls: list[ft.Control] = [
        ft.TextField(
            label="Título de la receta",
            value=text,
            autofocus=True,
            border_radius=8,
            on_change=lambda e: set_text(e.control.value),
            on_submit=lambda _: confirm(),
        )
    ]
    if hint:
        controls.insert(0, ft.Text(hint, size=13, color=theme.MUTED))

    ft.use_dialog(
        _alert(
            _title(title),
            _form_body(380, controls, error),
            confirm_label=confirm_label,
            confirm_color=theme.ACCENT,
            on_confirm=confirm,
            on_close=on_close,
        )
    )
    return ft.Container(visible=False)


@ft.component
def IngredientDialog(
    *,
    on_submit: Callable[[str, str, str], None],
    on_close: Callable[[], None],
) -> ft.Control:
    """``on_submit(nombre, cantidad, unidad)``; cantidad y unidad pueden venir vacías."""
    name, set_name = ft.use_state("")
    amount, set_amount = ft.use_state("")
    unit, set_unit = ft.use_state("")
    error, set_error = ft.use_state(None)

    def confirm() -> None:
        _submit_with_errors(lambda: on_submit(name, amount, unit), set_error)

    ft.use_dialog(
        _alert(
            _title("Agregar ingrediente"),
            _form_body(
                420,
                [
                    ft.Text(
                        "Si el ingrediente ya existe en tu catálogo, se reutilizará automáticamente.",
                        size=12,
                        color=theme.MUTED,
                    ),
                    ft.TextField(
                        label="Nombre del ingrediente",
                        hint_text="ej. Jitomate, Sal, Harina...",
                        value=name,
                        autofocus=True,
                        border_radius=8,
                        on_change=lambda e: set_name(e.control.value),
                    ),
                    ft.TextField(
                        label="Cantidad",
                        hint_text="ej. 2, 250, 1/2...",
                        value=amount,
                        border_radius=8,
                        on_change=lambda e: set_amount(e.control.value),
                    ),
                    ft.TextField(
                        label="Unidad de medida",
                        hint_text="ej. piezas, g, ml, tazas...",
                        value=unit,
                        border_radius=8,
                        on_change=lambda e: set_unit(e.control.value),
                        on_submit=lambda _: confirm(),
                    ),
                ],
                error,
            ),
            confirm_label="Agregar",
            confirm_color=theme.ACCENT,
            on_confirm=confirm,
            on_close=on_close,
        )
    )
    return ft.Container(visible=False)


@ft.component
def StepDialog(
    next_number: int,
    *,
    on_submit: Callable[[int, str], None],
    on_close: Callable[[], None],
) -> ft.Control:
    """``on_submit(número, instrucción)``."""
    number, set_number = ft.use_state(str(next_number))
    text, set_text = ft.use_state("")
    error, set_error = ft.use_state(None)

    def confirm() -> None:
        try:
            step_number = int(number.strip())
        except ValueError:
            set_error("El número de paso debe ser un entero mayor que cero.")
            return
        _submit_with_errors(lambda: on_submit(step_number, text), set_error)

    ft.use_dialog(
        _alert(
            _title("Agregar instrucción"),
            _form_body(
                440,
                [
                    ft.TextField(
                        label="Número de paso",
                        value=number,
                        width=100,
                        border_radius=8,
                        on_change=lambda e: set_number(e.control.value),
                    ),
                    ft.TextField(
                        label="Instrucción detallada",
                        value=text,
                        multiline=True,
                        min_lines=3,
                        max_lines=6,
                        autofocus=True,
                        border_radius=8,
                        on_change=lambda e: set_text(e.control.value),
                    ),
                ],
                error,
            ),
            confirm_label="Guardar paso",
            confirm_color=theme.ACCENT,
            on_confirm=confirm,
            on_close=on_close,
        )
    )
    return ft.Container(visible=False)


@ft.component
def ConfirmDeleteDialog(
    title: str,
    message: str,
    *,
    on_confirm: Callable[[], None],
    on_close: Callable[[], None],
) -> ft.Control:
    ft.use_dialog(
        _alert(
            _title(title, theme.DANGER),
            ft.Text(message),
            confirm_label="Eliminar",
            confirm_color=theme.DANGER,
            on_confirm=on_confirm,
            on_close=on_close,
        )
    )
    return ft.Container(visible=False)
