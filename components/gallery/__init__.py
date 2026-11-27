"""Galerías del catálogo y su registro de secciones."""

from collections.abc import Callable
from dataclasses import dataclass

import flet as ft

from .buttons import ButtonsGallery
from .cards import CardsGallery
from .colors import ColorsGallery
from .containers import ContainersGallery
from .gradients import GradientsGallery
from .icons import IconsGallery
from .inputs import InputsGallery
from .shimmer import ShimmerGallery
from .styled_buttons import StyledButtonsGallery
from .tables import TablesGallery


@dataclass(frozen=True)
class Section:
    """Una página del catálogo: nombre, icono de navegación y componente."""

    key: str
    title: str
    description: str
    icon: ft.IconData
    view: Callable[..., ft.Control]


SECTIONS: tuple[Section, ...] = (
    Section("buttons", "Buttons", "Átomos Button e IconButton.", ft.Icons.SMART_BUTTON, ButtonsGallery),
    Section("inputs", "Inputs", "TextInput, SearchInput y Surface.", ft.Icons.TEXT_FIELDS, InputsGallery),
    Section("styled", "Styled buttons", "Variantes visuales descritas con ButtonSpec.", ft.Icons.BRUSH, StyledButtonsGallery),
    Section("containers", "Containers", "Patrones con ft.Container.", ft.Icons.CHECK_BOX_OUTLINE_BLANK, ContainersGallery),
    Section("cards", "Cards", "Tarjetas de perfil, métrica, producto y más.", ft.Icons.CREDIT_CARD, CardsGallery),
    Section("tables", "Tables", "Variantes de ft.DataTable.", ft.Icons.TABLE_CHART_OUTLINED, TablesGallery),
    Section("gradients", "Gradients", "Gradientes lineales, radiales y angulares.", ft.Icons.GRADIENT, GradientsGallery),
    Section("shimmer", "Shimmer", "Skeletons de carga reutilizables.", ft.Icons.AUTO_AWESOME, ShimmerGallery),
    Section("colors", "Colors", "Todos los miembros de ft.Colors.", ft.Icons.PALETTE_OUTLINED, ColorsGallery),
    Section("icons", "Icons", "Todos los miembros de ft.Icons.", ft.Icons.EMOJI_SYMBOLS, IconsGallery),
)

__all__ = ["SECTIONS", "Section"]
