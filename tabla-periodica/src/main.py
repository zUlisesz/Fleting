import flet as ft
import json as js
import algorithm as alg
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def load_json(filename):
    with (BASE_DIR / filename).open("r", encoding="utf-8") as f:
        return js.load(f)


def normalize_symbol(value):
    return (value or "").strip().capitalize()

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "Tabla Periódica e Ingeniería de Materiales"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 30

    try:
        ELEMENTS_DATA = load_json("elements.json")
        PERIODIC_TABLE = load_json("table.json")
        GRADIENTS_DATA = load_json("colors.json")
    except FileNotFoundError as e:
        page.add(ft.Text(f"Error crítico: No se encontró el archivo {e.filename}", color="red", size=20))
        return

    element_buttons = {}

    ALIGNMENTS = {
        "top_left": ft.Alignment(-1, -1),
        "top_center": ft.Alignment(0, -1),
        "top_right": ft.Alignment(1, -1),
        "center": ft.Alignment(0, 0),
        "bottom_left": ft.Alignment(-1, 1),
        "bottom_center": ft.Alignment(0, 1),
        "bottom_right": ft.Alignment(1, 1),
    }
    
    def get_alignment(name):
        return ALIGNMENTS.get(name, ALIGNMENTS["center"])

    
    detail_name = ft.Text("Selecciona un elemento", size=30, weight=ft.FontWeight.BOLD)
    detail_info = ft.Text("Haz clic en un elemento para ver sus propiedades", size=16, text_align=ft.TextAlign.CENTER)
    detail_chem = ft.Text("", size=14, text_align=ft.TextAlign.CENTER, color=ft.Colors.WHITE_70, selectable=True)
    
    info_card = ft.Container(
        content=ft.Column(
            [detail_name, detail_info, ft.Divider(color=ft.Colors.WHITE_24), detail_chem],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        ),
        width=600,
        height=240,
        bgcolor=ft.Colors.BLUE_ACCENT,
        border_radius=15,
        padding=20,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK_45)
    )

    def analyze_combination(sym1, sym2):
        e1 = ELEMENTS_DATA.get(sym1)
        e2 = ELEMENTS_DATA.get(sym2)

        if not e1 or not e2:
            return "Introduce símbolos válidos (Ej: Si, P, B)"

        c1 = alg.calculate_chemistry_data(e1["number"])
        c2 = alg.calculate_chemistry_data(e2["number"])
        v1 = c1["valence"]
        v2 = c2["valence"]

        if v1 == 4 and v2 == 4:
            return "Semiconductor Intrínseco (Estructura pura)"

        if (v1 == 4 and v2 == 5) or (v1 == 5 and v2 == 4):
            return "Semiconductor Tipo N (Dopaje con exceso de e⁻)"

        if (v1 == 4 and v2 == 3) or (v1 == 3 and v2 == 4):
            return "Semiconductor Tipo P (Creación de huecos)"

        if v1 <= 3 and v2 <= 3:
            return "Material Conductor (Enlace Metálico)"

        if v1 >= 6 or v2 >= 6 or v1 == 8 or v2 == 8:
            return "Material Aislante / Dieléctrico"

        return "Combinación de Propiedades Mixtas"

    def show_details(e):
        symbol = e.control.data
        data = ELEMENTS_DATA.get(symbol)
        if data:
            atomic_number = data.get('number', 0)
            chem_data = alg.calculate_chemistry_data(atomic_number)

            detail_name.value = f"{symbol} — {data.get('name', 'Desconocido')}"
            detail_info.value = (
                f"Número Atómico: {atomic_number}   |   Masa: {data.get('mass', '?')} u\n"
                f"Categoría: {data.get('category', 'N/A')}"
            )
            if chem_data:
                detail_chem.value = (
                    f"Electrones de Valencia: {chem_data['valence']}   |   Huecos : {chem_data['holes']}\n\n"
                    f"Configuración Electrónica: {chem_data['configuration']}"
                )
            else:
                detail_chem.value = "No se pudo calcular la configuración electrónica."
        page.update()

    def handle_search(e):
        term = (e.control.value or "").strip().lower()
        for symbol, buttons in element_buttons.items():
            data = ELEMENTS_DATA.get(symbol, {})
            name = data.get("name", "").lower()
            match = term and (term in symbol.lower() or term in name)
            for btn in buttons:
                if not term:
                    btn.opacity, btn.scale = 1.0, 1.0
                elif match:
                    btn.opacity, btn.scale = 1.0, 1.15
                else:
                    btn.opacity, btn.scale = 0.15, 0.85
        page.update()

    input_a = ft.TextField(label="Elemento A", width=120, text_align="center")
    input_b = ft.TextField(label="Elemento B", width=120, text_align="center")
    result_text = ft.Text("", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_300)

    def handle_analyze(e):
        sym1 = normalize_symbol(input_a.value)
        sym2 = normalize_symbol(input_b.value)
        result_text.value = analyze_combination(sym1, sym2)
        page.update()

    analyze_box = ft.Container(
        content=ft.Column(
            [
                ft.Text("Dopaje y Materiales", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([input_a, input_b], alignment="center"),
                ft.Button("Analizar Unión", icon=ft.Icons.BOLT, on_click=handle_analyze),
                result_text,
            ],
            alignment="center", horizontal_alignment="center", spacing=10,
        ),
        width=600,
        height=240,
        border_radius=15, bgcolor=ft.Colors.GREY_900,
    )

    def create_element(symbol):
        if symbol is None: return ft.Container(width=55, height=55)
        data = ELEMENTS_DATA.get(symbol, {})
        category = data.get("category")
        grad_info = GRADIENTS_DATA.get(category)
        
        gradient = None
        if grad_info:
            gradient = ft.LinearGradient(
                begin=get_alignment(grad_info.get("begin")),
                end=get_alignment(grad_info.get("end")),
                colors=[getattr(ft.Colors, c) for c in grad_info.get("colors", [])],
            )

        btn = ft.Container(
            content=ft.Text(symbol, weight="bold", color="white", size=14),
            width=55, height=55, border_radius=8, alignment=ft.Alignment(0, 0),
            gradient=gradient, bgcolor=ft.Colors.GREY_800 if not gradient else None,
            data=symbol, on_click=show_details, animate_opacity=250, animate_scale=250,
            shadow=ft.BoxShadow(blur_radius=6, color="black45"),
        )
        element_buttons.setdefault(symbol, []).append(btn)
        return btn

    # Construcción Final
    search_field = ft.TextField(
        label="Buscar elemento...", on_change=handle_search,
        width=400, prefix_icon=ft.Icons.SEARCH, border_radius=10, bgcolor=ft.Colors.GREY_900
    )
    
    rows = [ft.Row([create_element(s) for s in row], alignment="center", spacing=8) for row in PERIODIC_TABLE]
    
    page.add(
        ft.Column(
            [
                ft.Text("TABLA PERIÓDICA ELEMENTAL", size=36, weight="bold", color=ft.Colors.BLUE_200),
                search_field,
                ft.Row([info_card, analyze_box], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                ft.Divider(height=20, color="transparent"),
                ft.Column(rows, spacing=8),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15,
        )
    )

if __name__ == "__main__":
    ft.run(main)
