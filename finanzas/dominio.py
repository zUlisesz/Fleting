"""Reglas de dominio de finanzas: importes, filtros y resúmenes"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal, InvalidOperation

CATEGORIAS = ("Comida", "Transporte", "Estudio", "Hogar", "Ocio", "Ahorro", "Trabajo", "Otros")
TIPOS = ("Gasto", "Ingreso")
TIPOS_FILTRO = ("Todos", *TIPOS)
CATEGORIAS_FILTRO = ("Todas", *CATEGORIAS)

MAX_IMPORTE = Decimal("9999999.99")
MAX_TEXTO = 80


def a_centavos(texto: str) -> int:
    """Convierte un importe positivo con hasta dos decimales a centavos."""
    if not isinstance(texto, str):
        raise ValueError("El importe debe ser texto.")
    limpio = texto.strip()
    if not re.fullmatch(r"\d+(?:[.,]\d{1,2})?", limpio):
        raise ValueError("Usa un importe positivo con hasta dos decimales, sin separador de miles.")
    try:
        valor = Decimal(limpio.replace(",", "."))
    except InvalidOperation as error:
        raise ValueError("Importe inválido.") from error
    if not Decimal("0") < valor <= MAX_IMPORTE:
        raise ValueError("El importe debe ser mayor que cero y no superar 9,999,999.99.")
    return int(valor * 100)


def moneda(centavos: int) -> str:
    """Formatea centavos como importe absoluto en pesos mexicanos."""
    centavos = abs(centavos)
    return f"${centavos // 100:,}.{centavos % 100:02d}"


def moneda_firmada(centavos: int) -> str:
    """Formatea un saldo conservando el signo deudor cuando existe."""
    return f"{'-' if centavos < 0 else ''}{moneda(centavos)}"


def validar_texto(valor: object, nombre: str) -> str:
    """Texto recortado de 1 a 80 caracteres; ``nombre`` se usa en el mensaje."""
    if not isinstance(valor, str):
        raise ValueError(f"El {nombre} debe ser texto.")
    limpio = valor.strip()
    if not 1 <= len(limpio) <= MAX_TEXTO:
        raise ValueError(f"El {nombre} debe tener entre 1 y {MAX_TEXTO} caracteres.")
    return limpio


def validar_fecha(fecha: object) -> str:
    """Fecha real en formato AAAA-MM-DD."""
    try:
        normal = date.fromisoformat(fecha).isoformat()  # type: ignore[arg-type]
    except (ValueError, TypeError) as error:
        raise ValueError("Introduce una fecha real en formato AAAA-MM-DD.") from error
    if normal != fecha:
        raise ValueError("Usa formato AAAA-MM-DD.")
    return normal


@dataclass(frozen=True)
class Filtros:
    """Criterios para listar movimientos; ``validar`` rechaza valores inválidos."""

    categoria: str = "Todas"
    mes: str = ""
    tipo: str = "Todos"

    def validar(self) -> "Filtros":
        if self.categoria not in CATEGORIAS_FILTRO:
            raise ValueError("Categoría de filtro inválida.")
        if self.tipo not in TIPOS_FILTRO:
            raise ValueError("Tipo de filtro inválido.")
        if self.mes:
            if not re.fullmatch(r"\d{4}-\d{2}", self.mes):
                raise ValueError("El mes debe tener formato AAAA-MM.")
            try:
                date.fromisoformat(self.mes + "-01")
            except ValueError as error:
                raise ValueError("Mes inválido.") from error
        return self

    @property
    def etiqueta(self) -> str:
        return f"{self.categoria} · {self.tipo} · {self.mes or 'todos los meses'}"


@dataclass(frozen=True)
class Movimiento:
    id: int
    fecha: str
    concepto: str
    categoria: str
    tipo: str
    centavos: int

    @property
    def es_ingreso(self) -> bool:
        return self.tipo == "Ingreso"


@dataclass(frozen=True)
class Resumen:
    """Totales de flujo de efectivo de un conjunto de movimientos."""

    ingresos: int = 0
    gastos: int = 0
    cantidad: int = 0
    categorias: dict[str, int] = field(default_factory=dict)

    @property
    def total(self) -> int:
        """Suma de importes absolutos; base de las proporciones por categoría."""
        return self.ingresos + self.gastos

    @property
    def balance(self) -> int:
        return self.ingresos - self.gastos


def resumir(movimientos: list[Movimiento]) -> Resumen:
    """Calcula ingresos, gastos y el total por «tipo · categoría»."""
    categorias: dict[str, int] = {}
    ingresos = gastos = 0
    for movimiento in movimientos:
        clave = f"{movimiento.tipo} · {movimiento.categoria}"
        categorias[clave] = categorias.get(clave, 0) + movimiento.centavos
        if movimiento.es_ingreso:
            ingresos += movimiento.centavos
        else:
            gastos += movimiento.centavos
    return Resumen(ingresos, gastos, len(movimientos), categorias)
