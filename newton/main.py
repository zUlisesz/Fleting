"""Newton Optimizer & Surface Visualizer: UI declarativa con Flet 1.0 (componentes y hooks).

    python3 -m newton.main        # desde la carpeta que contiene `newton/`
"""

import asyncio

import flet as ft

from .analysis import Analysis, Line, Tone, analyze

APP_TITLE = "Newton Optimizer & Surface Visualizer"
DEFAULT_FUNCTION = "(x-2)**4 + (x-2*y)**2"
DEFAULT_POINT = "0, 0"
IDLE_STATUS = Line("Escribe una función y presiona Optimizar.")
RUNNING_STATUS = Line("Calculando iteraciones y generando la superficie...")
PANEL_HEIGHT = 500

TONE_COLORS: dict[Tone, str | None] = {
    "normal": None,
    "good": ft.Colors.GREEN_700,
    "warning": ft.Colors.AMBER_800,
    "error": ft.Colors.RED_700,
}


def tone_text(line: Line, **kwargs) -> ft.Text:
    """``Text`` coloreado según el tono de la línea."""
    return ft.Text(line.text, color=TONE_COLORS[line.tone], **kwargs)


@ft.component
def Header() -> ft.Control:
    return ft.Column(
        spacing=2,
        controls=[
            ft.Text(APP_TITLE, size=32, weight=ft.FontWeight.BOLD),
            ft.Text("Explora el método de Newton para funciones de dos variables."),
        ],
    )


@ft.component
def ProblemForm(
    function_text: str,
    point_text: str,
    *,
    running: bool,
    on_function_change,
    on_point_change,
    on_optimize,
) -> ft.Control:
    """Función, punto inicial y botón para optimizar (``on_optimize`` es una corrutina)."""

    async def submit(_) -> None:
        await on_optimize()

    return ft.ResponsiveRow(
        controls=[
            ft.TextField(
                label="Función f(x, y)",
                value=function_text,
                helper="Usa exactamente dos variables, por ejemplo x e y.",
                col={"xs": 12, "md": 6},
                on_change=lambda e: on_function_change(e.control.value),
                on_submit=submit,
            ),
            ft.TextField(
                label="Punto inicial (x, y)",
                value=point_text,
                helper="Escribe dos números separados por una coma.",
                col={"xs": 12, "md": 3},
                on_change=lambda e: on_point_change(e.control.value),
                on_submit=submit,
            ),
            ft.Button(
                "Optimizar",
                icon=ft.Icons.PLAY_ARROW,
                disabled=running,
                col={"xs": 12, "md": 3},
                on_click=submit,
            ),
        ]
    )


@ft.component
def LogPanel(lines: tuple[Line, ...]) -> ft.Control:
    """Registro de iteraciones; la última línea (el resultado) va en negrita."""
    entries = [
        tone_text(line, weight=ft.FontWeight.BOLD if i == len(lines) - 1 else None)
        for i, line in enumerate(lines)
    ]
    return ft.Container(
        height=PANEL_HEIGHT,
        padding=16,
        border_radius=12,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text(value ="Registro de iteraciones", size=20, weight=ft.FontWeight.BOLD),
                ft.Column(controls=entries, scroll=ft.ScrollMode.AUTO, spacing=8, expand=True),
            ],
        ),
    )


@ft.component
def ChartPanel(analysis: Analysis | None, running: bool) -> ft.Control:
    """Gráfica 3D, o el motivo por el que no hay gráfica."""
    if running:
        content: ft.Control = ft.ProgressRing()
    elif analysis is None:
        content = ft.Text("La gráfica aparecerá aquí.", color=ft.Colors.GREY_600)
    elif analysis.image is None:
        content = ft.Text("No se pudo generar la gráfica.", color=ft.Colors.RED_700)
    else:
        content = ft.Image(src=analysis.image, fit=ft.BoxFit.CONTAIN, height=PANEL_HEIGHT - 20)
    return ft.Container(
        height=PANEL_HEIGHT,
        padding=10,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=12,
        alignment=ft.Alignment.CENTER,
        content=content,
    )


@ft.component
def App() -> ft.Control:
    function_text, set_function_text = ft.use_state(DEFAULT_FUNCTION)
    point_text, set_point_text = ft.use_state(DEFAULT_POINT)
    analysis, set_analysis = ft.use_state(None)  # Analysis | None
    running, set_running = ft.use_state(False)

    async def optimize() -> None:
        if running:
            return
        set_running(True)
        # El cálculo y el dibujo son pesados: fuera del hilo de la interfaz.
        result = await asyncio.to_thread(analyze, function_text, point_text)
        set_analysis(result)
        set_running(False)

    if running:
        status = RUNNING_STATUS
    elif analysis is None:
        status = IDLE_STATUS
    else:
        status = analysis.status

    return ft.Column(
        spacing=16,
        controls=[
            Header(),
            ft.Divider(),
            ProblemForm(
                function_text,
                point_text,
                running=running,
                on_function_change=set_function_text,
                on_point_change=set_point_text,
                on_optimize=optimize,
            ),
            tone_text(status),
            ft.ResponsiveRow(
                controls=[
                    # Los componentes no tienen `col`: se envuelven en un Container.
                    ft.Container(
                        col={"xs": 12, "md": 4},
                        content=LogPanel(() if running or analysis is None else analysis.log),
                    ),
                    ft.Container(
                        col={"xs": 12, "md": 8},
                        content=ChartPanel(analysis, running),
                    ),
                ]
            ),
        ],
    )


def main(page: ft.Page) -> None:
    page.title = APP_TITLE
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.window.width = 1100
    page.window.height = 850
    page.padding = 24
    page.scroll = ft.ScrollMode.AUTO
    page.render(App)


if __name__ == "__main__":
    ft.run(main)
