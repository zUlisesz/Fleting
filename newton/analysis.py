"""Caso de uso de la app: optimizar, describir el resultado y dibujarlo.

Devuelve datos simples (textos con un tono, bytes del PNG) para que la interfaz
solo tenga que mostrarlos.
"""

from dataclasses import dataclass
from typing import Literal

from .optimizer import LOCAL_MINIMUM, NewtonResult, solve_newton
from .plotting import render_surface

Tone = Literal["normal", "good", "warning", "error"]

# Errores de entrada o de evaluación que se explican al usuario.
EXPECTED_ERRORS = (ValueError, TypeError, OverflowError)


@dataclass(frozen=True)
class Line:
    """Un texto con el tono con el que debe mostrarse."""

    text: str
    tone: Tone = "normal"


@dataclass(frozen=True)
class Analysis:
    """Resultado listo para mostrar: estado, registro de iteraciones y gráfica."""

    status: Line
    log: tuple[Line, ...] = ()
    image: bytes | None = None

    @property
    def failed(self) -> bool:
        return self.image is None


def _final_tone(result: NewtonResult) -> Tone:
    """Un mínimo local es el mejor resultado; cualquier otro caso es una advertencia."""
    if result.converged and result.stationary_point_type == LOCAL_MINIMUM:
        return "good"
    return "warning"


def iteration_log(result: NewtonResult) -> tuple[Line, ...]:
    """Una línea por iteración y una de cierre con el resultado."""
    lines = [
        Line(f"Iteración {n}: ({point[0]:.4f}, {point[1]:.4f})")
        for n, point in enumerate(result.history[1:], start=1)
    ]
    if result.converged:
        summary = (
            f"Convergencia alcanzada en {result.iterations} iteración(es). "
            f"Clasificación: {result.stationary_point_type}."
        )
    else:
        summary = f"Se alcanzaron {result.iterations} iteraciones sin cumplir la tolerancia."
    lines.append(Line(summary, _final_tone(result)))
    return tuple(lines)


def status_line(result: NewtonResult) -> Line:
    if result.converged:
        return Line(f"Punto estacionario: {result.stationary_point_type}.", _final_tone(result))
    return Line("Resultado generado sin convergencia.", "warning")


def analyze(expression_text: str, point_text: str) -> Analysis:
    """Optimiza con Newton y dibuja el resultado; los errores de entrada no se propagan."""
    try:
        result = solve_newton(expression_text, point_text)
        image = render_surface(result)
    except EXPECTED_ERRORS as error:
        return Analysis(Line(f"No se pudo optimizar: {error}", "error"))
    return Analysis(status_line(result), iteration_log(result), image)
