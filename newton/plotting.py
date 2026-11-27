"""Dibujo de la superficie y la trayectoria de Newton"""

from io import BytesIO

import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

from .optimizer import NewtonResult, evaluate_surface

PLOT_SIZE = 40  # puntos por eje en la malla
PLOT_RADIUS = 8  # semiancho de la región dibujada alrededor del resultado


def render_surface(result: NewtonResult) -> bytes:
    """Dibuja la superficie y la trayectoria; devuelve un PNG en memoria."""
    center_x, center_y = result.point
    x_range = np.linspace(center_x - PLOT_RADIUS, center_x + PLOT_RADIUS, PLOT_SIZE)
    y_range = np.linspace(center_y - PLOT_RADIUS, center_y + PLOT_RADIUS, PLOT_SIZE)
    x_mesh, y_mesh = np.meshgrid(x_range, y_range)
    z_mesh = evaluate_surface(result, x_mesh, y_mesh)

    figure = Figure(figsize=(6, 4.5), tight_layout=True)
    axes = figure.add_subplot(111, projection="3d")
    axes.plot_surface(x_mesh, y_mesh, z_mesh, cmap="viridis", alpha=0.7, edgecolor="none")

    history = np.asarray(result.history)
    axes.plot(
        history[:, 0],
        history[:, 1],
        evaluate_surface(result, history[:, 0], history[:, 1]),
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
