from io import BytesIO

import flet as ft
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

try:
    from .optimizer import NewtonResult, evaluate_surface, solve_newton
except ImportError:  # Allows: python newton/app.py
    from optimizer import NewtonResult, evaluate_surface, solve_newton


APP_TITLE = "Newton Optimizer & Surface Visualizer"
PLOT_SIZE = 40
PLOT_RADIUS = 8


def render_surface(result: NewtonResult) -> bytes:
    """Render the function surface and Newton path as a PNG held in memory."""
    center_x, center_y = result.point
    x_range = np.linspace(center_x - PLOT_RADIUS, center_x + PLOT_RADIUS, PLOT_SIZE)
    y_range = np.linspace(center_y - PLOT_RADIUS, center_y + PLOT_RADIUS, PLOT_SIZE)
    x_mesh, y_mesh = np.meshgrid(x_range, y_range)
    z_mesh = evaluate_surface(result, x_mesh, y_mesh)

    figure = Figure(figsize=(6, 4.5), tight_layout=True)
    axes = figure.add_subplot(111, projection="3d")
    axes.plot_surface(x_mesh, y_mesh, z_mesh, cmap="viridis", alpha=0.7, edgecolor="none")

    history = np.asarray(result.history)
    z_history = evaluate_surface(result, history[:, 0], history[:, 1])
    axes.plot(
        history[:, 0],
        history[:, 1],
        z_history,
        color="purple",
        marker="o",
        markersize=4,
        label="Trayectoria",
    )
    axes.set_title("Superficie y trayectoria de Newton")
    axes.set_xlabel(result.variables[0].name)
    axes.set_ylabel(result.variables[1].name)
    axes.legend()

    image = BytesIO()
    FigureCanvasAgg(figure).print_png(image)
    return image.getvalue()


def iteration_log(result: NewtonResult) -> list[ft.Control]:
    """Create the controls that describe each Newton iteration."""
    controls: list[ft.Control] = []
    for iteration, point in enumerate(result.history[1:], start=1):
        controls.append(ft.Text(f"Iteración {iteration}: ({point[0]:.4f}, {point[1]:.4f})"))

    if result.converged:
        controls.append(
            ft.Text(
                f"Convergencia alcanzada en {result.iterations} iteración(es).",
                color=ft.Colors.GREEN,
                weight=ft.FontWeight.BOLD,
            )
        )
    else:
        controls.append(
            ft.Text(
                f"Se alcanzaron {result.iterations} iteraciones sin cumplir la tolerancia.",
                color=ft.Colors.AMBER,
                weight=ft.FontWeight.BOLD,
            )
        )

    return controls


class NewtonApp:
    """Coordinates the Flet controls and the Newton optimization logic."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.function_input = ft.TextField(
            label="Función f(x, y)",
            value="(x-2)**4 + (x-2*y)**2",
            helper="Usa exactamente dos variables, por ejemplo x e y.",
        )
        self.point_input = ft.TextField(
            label="Punto inicial (x, y)",
            value="0, 0",
            helper="Escribe dos números separados por una coma.",
        )
        self.status = ft.Text("Escribe una función y presiona Optimizar.")
        self.results = ft.Column(scroll=ft.ScrollMode.AUTO, height=410, spacing=8)
        self.chart = ft.Container(
            content=ft.Text("La gráfica aparecerá aquí.", color=ft.Colors.GREY_400),
            alignment=ft.Alignment.CENTER,
            height=500,
        )

    def build(self) -> None:
        """Build the GUI using the layout conventions of this repository."""
        self.page.title = APP_TITLE
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
        self.page.window.width = 1100
        self.page.window.height = 850
        self.page.padding = 24
        self.page.scroll = ft.ScrollMode.AUTO

        self.function_input.col = {"xs": 12, "md": 6}
        self.point_input.col = {"xs": 12, "md": 3}
        optimize_button = ft.Button(
            "Optimizar",
            icon=ft.Icons.PLAY_ARROW,
            on_click=self._optimize,
        )
        optimize_button.col = {"xs": 12, "md": 3}

        log_panel = ft.Container(
            col={"xs": 12, "md": 4},
            height=500,
            padding=16,
            border_radius=12,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            content=ft.Column(
                [
                    ft.Text("Registro de iteraciones", size=20, weight=ft.FontWeight.BOLD),
                    self.results,
                ],
                spacing=12,
            ),
        )
        chart_panel = ft.Container(
            col={"xs": 12, "md": 8},
            height=500,
            padding=10,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=12,
            content=self.chart,
        )

        self.page.add(
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(APP_TITLE, size=32, weight=ft.FontWeight.BOLD),
                            ft.Text("Explora el método de Newton para funciones de dos variables."),
                        ],
                        spacing=2,
                    ),
                ],
                tight=True,
                spacing=12,
                wrap=True,
            ),
            ft.Divider(),
            ft.ResponsiveRow([self.function_input, self.point_input, optimize_button]),
            self.status,
            ft.ResponsiveRow([log_panel, chart_panel]),
        )

    def _optimize(self, _: ft.Event[ft.Button]) -> None:
        self.results.controls.clear()
        self.status.value = "Calculando iteraciones y generando la superficie..."
        self.status.color = None
        self.chart.content = ft.ProgressRing()
        self.page.update()

        try:
            result = solve_newton(self.function_input.value or "", self.point_input.value or "")
            self.results.controls.extend(iteration_log(result))
            self.chart.content = ft.Image(
                src=render_surface(result),
                fit=ft.BoxFit.CONTAIN,
                height=480,
            )
            self.status.value = "Resultado generado." if result.converged else "Resultado generado sin convergencia."
            self.status.color = ft.Colors.GREEN_700 if result.converged else ft.Colors.AMBER_800
        except (ValueError, TypeError, OverflowError) as error:
            self.status.value = f"No se pudo optimizar: {error}"
            self.status.color = ft.Colors.RED_700
            self.chart.content = ft.Text("No se pudo generar la gráfica.", color=ft.Colors.RED)

        self.page.update()


def main(page: ft.Page) -> None:
    """Create the desktop GUI from the Flet library entry point."""
    app = NewtonApp(page)
    app.build()


if __name__ == "__main__":
    ft.run(main)
