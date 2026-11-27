"""Suma de números binarios, sin dependencias de Flet.

``sumar`` devuelve también los acarreos de cada columna, para poder mostrar la
suma "en papel" como se hace a mano.
"""

from dataclasses import dataclass

MAX_BITS = 16
INVALID_MESSAGE = "Escribe solo ceros y unos."


def es_binario(valor: str) -> bool:
    """Cadena no vacía formada solo por ``0`` y ``1``."""
    return isinstance(valor, str) and bool(valor) and set(valor) <= {"0", "1"}


@dataclass(frozen=True)
class Suma:
    """Suma de dos binarios con el detalle columna por columna.

    ``primero`` y ``segundo`` son los sumandos tal como se escribieron;
    ``acarreos`` y ``resultado`` tienen ``ancho`` bits (uno más que el sumando más
    largo). Alineados a la derecha, el bit ``i`` de cada fila pertenece a la misma
    columna; ``acarreos`` guarda el acarreo que *entra* a cada columna.
    """

    primero: str
    segundo: str
    acarreos: str
    resultado: str

    @property
    def ancho(self) -> int:
        return len(self.resultado)

    @property
    def decimal(self) -> tuple[int, int, int]:
        return int(self.primero, 2), int(self.segundo, 2), int(self.resultado, 2)


def sumar(primero: str, segundo: str) -> Suma:
    """Suma dos binarios; lanza ``ValueError`` si alguno no es válido o es muy largo."""
    for valor in (primero, segundo):
        if not es_binario(valor):
            raise ValueError(INVALID_MESSAGE)
        if len(valor) > MAX_BITS:
            raise ValueError(f"Máximo {MAX_BITS} bits por número.")

    ancho = max(len(primero), len(segundo)) + 1  # la suma puede ganar un bit
    bits, acarreos, acarreo = [], [], 0
    for x, y in zip(reversed(primero.zfill(ancho)), reversed(segundo.zfill(ancho))):
        acarreos.append(str(acarreo))
        total = int(x) + int(y) + acarreo
        bits.append(str(total % 2))
        acarreo = total // 2

    return Suma(primero, segundo, "".join(reversed(acarreos)), "".join(reversed(bits)))
