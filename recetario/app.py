import flet as ft
from typing import Optional, List, Dict, Any
from services.recipe_service import RecipeService


def main(page: ft.Page):
    page.title = "Recetario Personal"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.GREY_50
    page.window.min_width = 850
    page.window.min_height = 650

    current_recipe_id: Optional[str] = None
    all_recipes_cache: List[Dict[str, Any]] = []

    def notify(message: str, is_error: bool = False):
        snack = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500),
            bgcolor=ft.Colors.RED_600 if is_error else ft.Colors.GREEN_700,
            duration=3000
        )
        page.show_dialog(snack)


    recipe_list_column = ft.Column(
        spacing=8,
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    search_input = ft.TextField(
        hint_text="Buscar recetas...",
        prefix_icon=ft.Icons.SEARCH,
        dense=True,
        border_radius=12,
        bgcolor=ft.Colors.WHITE,
        border_color=ft.Colors.GREY_300,
        expand=True
    )

    detail_container = ft.Container(
        expand=True,
        padding=ft.Padding(left=28, top=20, right=28, bottom=20),
        bgcolor=ft.Colors.GREY_100
    )

    def select_recipe(recipe_id: str):
        nonlocal current_recipe_id
        current_recipe_id = recipe_id
        render_recipe_list()
        render_recipe_detail()

    def render_recipe_list():
        query = (search_input.value or "").strip().lower()
        recipe_list_column.controls.clear()

        filtered = [
            r for r in all_recipes_cache
            if query in r["title"].lower()
        ]

        if not filtered:
            recipe_list_column.controls.append(
                ft.Container(
                    alignment=ft.Alignment.CENTER,
                    padding=20,
                    content=ft.Text(
                        "No se encontraron recetas" if query else "Aún no tienes recetas registradas",
                        color=ft.Colors.GREY_500,
                        size=13,
                        italic=True,
                        text_align=ft.TextAlign.CENTER
                    )
                )
            )
        else:
            for r in filtered:
                is_selected = (r["id"] == current_recipe_id)
                rec_id = r["id"]

                def make_click_handler(rid):
                    return lambda e: select_recipe(rid)

                item = ft.Container(
                    padding=ft.Padding(left=14, top=12, right=14, bottom=12),
                    border_radius=12,
                    bgcolor=ft.Colors.TEAL_50 if is_selected else ft.Colors.WHITE,
                    border=ft.Border.all(
                        1.5 if is_selected else 1,
                        ft.Colors.TEAL_600 if is_selected else ft.Colors.GREY_200
                    ),
                    ink=True,
                    on_click=make_click_handler(rec_id),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Row(
                                spacing=10,
                                controls=[
                                    ft.Icon(
                                        ft.Icons.MENU_BOOK_ROUNDED,
                                        size=20,
                                        color=ft.Colors.TEAL_700 if is_selected else ft.Colors.GREY_600
                                    ),
                                    ft.Text(
                                        r["title"],
                                        size=14,
                                        weight=ft.FontWeight.W_600 if is_selected else ft.FontWeight.W_500,
                                        color=ft.Colors.TEAL_900 if is_selected else ft.Colors.GREY_800
                                    ),
                                ]
                            ),
                            ft.Icon(
                                ft.Icons.CHEVRON_RIGHT_ROUNDED,
                                size=18,
                                color=ft.Colors.TEAL_600 if is_selected else ft.Colors.GREY_400
                            )
                        ]
                    )
                )
                recipe_list_column.controls.append(item)

        page.update()

    def reload_recipes():
        nonlocal all_recipes_cache, current_recipe_id
        all_recipes_cache = RecipeService.get_all_recipes()

        # If current selected recipe is no longer available, select first or reset
        if current_recipe_id and not any(r["id"] == current_recipe_id for r in all_recipes_cache):
            current_recipe_id = all_recipes_cache[0]["id"] if all_recipes_cache else None
        elif not current_recipe_id and all_recipes_cache:
            current_recipe_id = all_recipes_cache[0]["id"]

        render_recipe_list()
        render_recipe_detail()

    search_input.on_change = lambda e: render_recipe_list()

    def open_new_recipe_dialog(e=None):
        name_field = ft.TextField(
            label="Título de la receta",
            autofocus=True,
            border_radius=8
        )

        def close_dialog(evt=None):
            page.pop_dialog()

        def save_recipe(evt):
            title = (name_field.value or "").strip()
            if not title:
                notify("Ingresa un título para la receta", is_error=True)
                return
            new_r = RecipeService.create_recipe(title)
            nonlocal current_recipe_id
            current_recipe_id = new_r.id
            page.pop_dialog()
            notify(f"Receta '{title}' creada exitosamente")
            reload_recipes()

        dialog = ft.AlertDialog(
            title=ft.Text("Nueva Receta", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                width=380,
                content=ft.Column(
                    spacing=12,
                    controls=[
                        ft.Text("Escribe el nombre de tu platillo:", size=13, color=ft.Colors.GREY_600),
                        name_field
                    ]
                )
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.FilledButton(
                    content=ft.Text("Guardar"),
                    bgcolor=ft.Colors.TEAL_600,
                    on_click=save_recipe
                )
            ]
        )
        page.show_dialog(dialog)

    def open_edit_recipe_dialog(recipe_id: str, current_title: str):
        name_field = ft.TextField(
            label="Título de la receta",
            value=current_title,
            autofocus=True,
            border_radius=8
        )

        def close_dialog(evt=None):
            page.pop_dialog()

        def save_edited(evt):
            title = (name_field.value or "").strip()
            if not title:
                notify("El título no puede estar vacío", is_error=True)
                return
            RecipeService.update_recipe_title(recipe_id, title)
            page.pop_dialog()
            notify("Título de receta actualizado")
            reload_recipes()

        dialog = ft.AlertDialog(
            title=ft.Text("Editar Receta", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                width=380,
                content=name_field
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.FilledButton(
                    content=ft.Text("Actualizar"),
                    bgcolor=ft.Colors.TEAL_600,
                    on_click=save_edited
                )
            ]
        )
        page.show_dialog(dialog)

    def confirm_delete_recipe(recipe_id: str, title: str):
        def close_dialog(evt=None):
            page.pop_dialog()

        def do_delete(evt):
            RecipeService.delete_recipe(recipe_id)
            page.pop_dialog()
            notify(f"Receta '{title}' eliminada")
            reload_recipes()

        dialog = ft.AlertDialog(
            title=ft.Text("Eliminar Receta", weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700),
            content=ft.Text(f"¿Estás seguro de que deseas eliminar la receta '{title}'? Esta acción no se puede deshacer."),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.FilledButton(
                    content=ft.Text("Eliminar"),
                    bgcolor=ft.Colors.RED_600,
                    on_click=do_delete
                )
            ]
        )
        page.show_dialog(dialog)

    def open_add_ingredient_dialog(recipe_id: str):
        name_field = ft.TextField(
            label="Nombre del ingrediente",
            hint_text="ej. Jitomate, Sal, Harina...",
            autofocus=True,
            border_radius=8
        )
        amount_field = ft.TextField(
            label="Cantidad",
            hint_text="ej. 2, 250, 1/2...",
            border_radius=8
        )
        unit_field = ft.TextField(
            label="Unidad de medida",
            hint_text="ej. piezas, g, ml, tazas...",
            border_radius=8
        )

        def close_dialog(evt=None):
            page.pop_dialog()

        def save_ingredient(evt):
            name = (name_field.value or "").strip()
            amount = (amount_field.value or "").strip() or None
            unit = (unit_field.value or "").strip() or None

            if not name:
                notify("Ingresa el nombre del ingrediente", is_error=True)
                return

            RecipeService.add_ingredient_to_recipe(
                recipe_id=recipe_id,
                ingredient_name=name,
                amount=amount,
                unit=unit
            )
            page.pop_dialog()
            notify(f"Ingrediente '{name}' agregado")
            render_recipe_detail()

        dialog = ft.AlertDialog(
            title=ft.Text("Agregar Ingrediente", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                width=420,
                content=ft.Column(
                    spacing=12,
                    controls=[
                        ft.Text(
                            "Si el ingrediente ya existe en tu catálogo, se reutilizará automáticamente.",
                            size=12,
                            color=ft.Colors.GREY_600
                        ),
                        name_field,
                        amount_field,
                        unit_field
                    ]
                )
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.FilledButton(
                    content=ft.Text("Agregar"),
                    bgcolor=ft.Colors.TEAL_600,
                    on_click=save_ingredient
                )
            ]
        )
        page.show_dialog(dialog)

    def open_add_step_dialog(recipe_id: str, next_step_num: int):
        step_field = ft.TextField(
            label="Número de paso",
            value=str(next_step_num),
            width=100,
            border_radius=8
        )
        instruction_field = ft.TextField(
            label="Instrucción detallada",
            multiline=True,
            min_lines=3,
            max_lines=6,
            autofocus=True,
            border_radius=8
        )

        def close_dialog(evt=None):
            page.pop_dialog()

        def save_step(evt):
            inst = (instruction_field.value or "").strip()
            if not inst:
                notify("Escribe la instrucción del paso", is_error=True)
                return
            try:
                num = int((step_field.value or "").strip())
            except ValueError:
                num = next_step_num

            RecipeService.add_step(
                recipe_id=recipe_id,
                step_number=num,
                instruction_text=inst
            )
            page.pop_dialog()
            notify("Paso añadido con éxito")
            render_recipe_detail()

        dialog = ft.AlertDialog(
            title=ft.Text("Agregar Instrucción", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                width=440,
                content=ft.Column(
                    spacing=12,
                    controls=[
                        step_field,
                        instruction_field
                    ]
                )
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.FilledButton(
                    content=ft.Text("Guardar Paso"),
                    bgcolor=ft.Colors.TEAL_600,
                    on_click=save_step
                )
            ]
        )
        page.show_dialog(dialog)

    def render_recipe_detail():
        if not current_recipe_id:
            detail_container.content = ft.Container(
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
                            color=ft.Colors.GREY_500
                        ),
                        ft.FilledButton(
                            content=ft.Text("Crear Primera Receta"),
                            icon=ft.Icons.ADD,
                            bgcolor=ft.Colors.TEAL_600,
                            on_click=open_new_recipe_dialog
                        )
                    ]
                )
            )
            page.update()
            return

        recipe = RecipeService.get_recipe_detail(current_recipe_id)
        if not recipe:
            current_recipe_id_val = None
            render_recipe_detail()
            return

        rid = recipe["id"]
        title = recipe["title"]
        ingredients = recipe.get("ingredients", [])
        instructions = recipe.get("instructions", [])

        # Header controls
        header = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            padding=10,
                            bgcolor=ft.Colors.TEAL_100,
                            border_radius=12,
                            content=ft.Icon(ft.Icons.DINNER_DINING, color=ft.Colors.TEAL_800, size=28)
                        ),
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(
                                    title,
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.GREY_900
                                ),
                                ft.Text(
                                    f"ID: {rid[:8]}...",
                                    size=11,
                                    color=ft.Colors.GREY_400
                                )
                            ]
                        )
                    ]
                ),
                ft.Row(
                    spacing=6,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.EDIT_OUTLINED,
                            tooltip="Editar título",
                            icon_color=ft.Colors.GREY_700,
                            on_click=lambda e: open_edit_recipe_dialog(rid, title)
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                            tooltip="Eliminar receta",
                            icon_color=ft.Colors.RED_500,
                            on_click=lambda e: confirm_delete_recipe(rid, title)
                        )
                    ]
                )
            ]
        )

        # Ingredients Section
        ingredient_items = []
        if not ingredients:
            ingredient_items.append(
                ft.Container(
                    padding=16,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(
                        "No has agregado ingredientes aún.",
                        size=13,
                        color=ft.Colors.GREY_500,
                        italic=True
                    )
                )
            )
        else:
            for ing in ingredients:
                link_id = ing["link_id"]
                unit_str = f" {ing['unit']}" if ing.get("unit") else ""
                amount_str = f"{ing['amount']}{unit_str}" if ing.get("amount") else (ing.get("unit") or "")

                def make_delete_ing(lid, iname):
                    return lambda e: delete_ingredient_link(lid, iname)

                ingredient_items.append(
                    ft.Container(
                        padding=ft.Padding(left=12, top=8, right=8, bottom=8),
                        border_radius=8,
                        bgcolor=ft.Colors.WHITE,
                        border=ft.Border.all(1, ft.Colors.GREY_200),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Row(
                                    spacing=8,
                                    controls=[
                                        ft.Icon(ft.Icons.CIRCLE, size=8, color=ft.Colors.TEAL_600),
                                        ft.Text(ing["name"], weight=ft.FontWeight.W_600, size=13, color=ft.Colors.GREY_800),
                                        ft.Text(f"— {amount_str}" if amount_str else "", size=13, color=ft.Colors.GREY_600),
                                    ]
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    icon_size=16,
                                    tooltip="Quitar ingrediente",
                                    icon_color=ft.Colors.GREY_500,
                                    on_click=make_delete_ing(link_id, ing["name"])
                                )
                            ]
                        )
                    )
                )

        ingredients_card = ft.Card(
            elevation=0.5,
            bgcolor =ft.Colors.GREY_100,
            shape=ft.RoundedRectangleBorder(radius=14),
            content=ft.Container(
                padding=16,
                content=ft.Column(
                    spacing=12,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Row(
                                    spacing=8,
                                    controls=[
                                        ft.Icon(ft.Icons.ECO_ROUNDED, size=20, color=ft.Colors.GREEN_700),
                                        ft.Text("Ingredientes", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                                        ft.Container(
                                            padding=ft.Padding(left=8, top=2, right=8, bottom=2),
                                            bgcolor=ft.Colors.GREEN_50,
                                            border_radius=10,
                                            content=ft.Text(str(len(ingredients)), size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800)
                                        )
                                    ]
                                ),
                                ft.FilledButton(
                                    content=ft.Text("Agregar", size=12),
                                    icon=ft.Icons.ADD,
                                    height=32,
                                    bgcolor=ft.Colors.TEAL_700,
                                    on_click=lambda e: open_add_ingredient_dialog(rid)
                                )
                            ]
                        ),
                        ft.Column(spacing=6, controls=ingredient_items)
                    ]
                )
            )
        )

        # Instructions Section
        instruction_items = []
        if not instructions:
            instruction_items.append(
                ft.Container(
                    padding=16,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(
                        "No has agregado pasos o instrucciones aún.",
                        size=13,
                        color=ft.Colors.GREY_500,
                        italic=True
                    )
                )
            )
        else:
            for step in instructions:
                step_id = step["id"]
                step_num = step["step_number"]
                inst_text = step["instruction"]

                def make_delete_step(sid, snum):
                    return lambda e: delete_instruction_step(sid, snum)

                instruction_items.append(
                    ft.Container(
                        padding=12,
                        border_radius=8,
                        bgcolor=ft.Colors.WHITE,
                        border=ft.Border.all(1, ft.Colors.GREY_200),
                        content=ft.Row(
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
                                            bgcolor=ft.Colors.TEAL_600,
                                            alignment=ft.Alignment.CENTER,
                                            content=ft.Text(
                                                str(step_num),
                                                color=ft.Colors.WHITE,
                                                size=12,
                                                weight=ft.FontWeight.BOLD
                                            )
                                        ),
                                        ft.Container(
                                            expand=True,
                                            content=ft.Text(
                                                inst_text,
                                                size=13,
                                                color=ft.Colors.GREY_800,
                                                selectable=True
                                            )
                                        )
                                    ]
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                    icon_size=18,
                                    tooltip="Eliminar paso",
                                    icon_color=ft.Colors.GREY_500,
                                    on_click=make_delete_step(step_id, step_num)
                                )
                            ]
                        )
                    )
                )

        next_step_num = (max([s["step_number"] for s in instructions]) + 1) if instructions else 1

        instructions_card = ft.Card(
            elevation=0.5,
            bgcolor=ft.Colors.GREY_100,
            shape=ft.RoundedRectangleBorder(radius=14),
            content=ft.Container(
                padding=16,
                content=ft.Column(
                    spacing=12,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Row(
                                    spacing=8,
                                    controls=[
                                        ft.Icon(ft.Icons.FORMAT_LIST_NUMBERED_ROUNDED, size=20, color=ft.Colors.TEAL_700),
                                        ft.Text("Preparación y Pasos", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                                        ft.Container(
                                            padding=ft.Padding(left=8, top=2, right=8, bottom=2),
                                            bgcolor=ft.Colors.TEAL_50,
                                            border_radius=10,
                                            content=ft.Text(str(len(instructions)), size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.TEAL_800)
                                        )
                                    ]
                                ),
                                ft.FilledButton(
                                    content=ft.Text("Agregar Paso", size=12),
                                    icon=ft.Icons.ADD,
                                    height=32,
                                    bgcolor=ft.Colors.TEAL_700,
                                    on_click=lambda e: open_add_step_dialog(rid, next_step_num)
                                )
                            ]
                        ),
                        ft.Column(spacing=8, controls=instruction_items)
                    ]
                )
            )
        )

        detail_container.content = ft.ListView(
            expand=True,
            spacing=16,
            controls=[
                header,
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                ingredients_card,
                instructions_card
            ]
        )
        page.update()

    def delete_ingredient_link(link_id: str, ingredient_name: str):
        RecipeService.remove_ingredient_from_recipe(link_id)
        notify(f"Ingrediente '{ingredient_name}' removido de la receta")
        render_recipe_detail()

    def delete_instruction_step(instruction_id: str, step_num: int):
        RecipeService.delete_step(instruction_id)
        notify(f"Paso #{step_num} eliminado")
        render_recipe_detail()


    sidebar = ft.Container(
        width=320,
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.only(right=ft.BorderSide(1, ft.Colors.GREY_300)),
        padding=ft.Padding(left=18, top=20, right=18, bottom=20),
        content=ft.Column(
            spacing=14,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            spacing=8,
                            controls=[
                                ft.Icon(ft.Icons.BOOK_ROUNDED, color=ft.Colors.TEAL_700, size=24),
                                ft.Text("Recetario", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_900),
                            ]
                        ),
                        ft.IconButton(
                            icon=ft.Icons.ADD_ROUNDED,
                            icon_color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.TEAL_700,
                            tooltip="Nueva Receta",
                            on_click=open_new_recipe_dialog
                        )
                    ]
                ),
                ft.Row(controls=[search_input]),
                ft.Text("MIS RECETAS", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500),
                recipe_list_column
            ]
        )
    )

    # Main screen layout
    page.add(
        ft.Row(
            spacing=0,
            expand=True,
            controls=[
                sidebar,
                detail_container
            ]
        )
    )

    reload_recipes()


if __name__ == "__main__":
    ft.run(main)
