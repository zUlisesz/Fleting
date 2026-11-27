"""Reglas de negocio del cajero automático"""
from dataclasses import dataclass, field

SALDO_INICIAL = 50_000
MONTO_MINIMO = 100
MONTO_MAXIMO = 6_000
MULTIPLO = 100
DENOMINACIONES = (1_000, 500, 200, 100, 50)  # de mayor a menor


def _es_entero(valor: object) -> bool:
    """True solo para ``int`` reales (``bool`` hereda de ``int`` y se descarta)."""
    return type(valor) is int

@dataclass
class Cajero:
    """Bóveda del cajero: valida retiros y entrega billetes exactos."""

    dinero: int = SALDO_INICIAL
    max_monto: int = MONTO_MAXIMO
    billetes: tuple[int, ...] = field(default=DENOMINACIONES)

    def actualizar_dinero(self, monto: int) -> None:
        """Descuenta un retiro sin permitir saldos inconsistentes."""
        if not _es_entero(monto) or monto < 0:
            raise ValueError("El monto a descontar debe ser un entero no negativo.")
        if monto > self.dinero:
            raise ValueError("El monto a descontar supera el saldo del cajero.")
        self.dinero -= monto

    def _error_retiro(self, monto: object) -> str | None:
        """Motivo por el que el retiro se rechaza, o ``None`` si es válido."""
        if not _es_entero(monto):
            return "Monto inválido"
        if monto > self.max_monto:
            return f"Monto máximo $ {self.max_monto}"
        if monto < MONTO_MINIMO:
            return f"El retiro mínimo es de $ {MONTO_MINIMO}"
        if monto > self.dinero:
            return "Saldo del cajero insuficiente"
        if monto % MULTIPLO:
            return "Monto inválido"
        return None

    def autorizar_retiro(self, monto: int) -> bool:
        """Indica si el retiro cumple todas las reglas del cajero."""
        return self._error_retiro(monto) is None

    def mensaje_retiro(self, monto: int) -> tuple[str, bool]:
        """Devuelve ``(mensaje, autorizado)`` para el intento de retiro."""
        error = self._error_retiro(monto)
        if error is not None:
            return error, False
        return f"Retiro por $ {monto} exitoso", True

    def entregar_dinero(self, monto: int) -> list[int]:
        """Entrega un retiro autorizado con billetes que suman exactamente ``monto``.

        Devuelve ``[]`` si el retiro no es válido. Descuenta el saldo solo
        cuando la entrega es exacta.
        """
        if not self.autorizar_retiro(monto):
            return []

        pendiente = monto
        entregados: list[int] = []
        for denominacion in sorted(self.billetes, reverse=True):
            cantidad, pendiente = divmod(pendiente, denominacion)
            entregados.extend([denominacion] * cantidad)

        if pendiente:
            raise ValueError(
                "No se puede entregar el monto con las denominaciones disponibles."
            )

        self.actualizar_dinero(monto)
        return entregados
