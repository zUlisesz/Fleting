class Cajero:

    def __init__(self):
        self.dinero : int = 50_000
        self.max_monto : int = 6_000
        self.billetes = (50, 100, 200, 500, 1000)

    def actualizar_dinero(self, monto : int) :
        '''Actualiza el estado de cajero'''
        self.dinero -= monto

    def autorizar_retiro(self, monto: int ) -> bool:
        """Regrea un valor de True si se cumplen todas las condiciones\n
        de otra manera se regesa un valor False"""
        if monto > self.max_monto or monto < 100: return False
        if monto > self.dinero: return False
        if monto % 100 != 0 :return False
        return True
    
    def mesaje_retiro(self, monto : int ) :
        """
        Descripción\n
        :monto: int -> Recibe un número entero representando el monto a retirar\n
        :return: str -> 'Devuelve un mensaje de status sobre el intento de retiro
        """
        if monto > self.max_monto: return f'Monto máximo $ {self.max_monto}', False
        if monto < 100 : return 'El retiro mínimo es de $ 100', False
        if monto > self.dinero: return 'Saldo del cajero insuficiente', False
        if monto % 100!= 0 : return 'Monto inválido', False
        return f'Retiro por $ {monto} exitoso' , True

    def entregar_dinero(self, monto: int) -> list[int]:
        """Entrega un importe autorizado con billetes que siempre suman el retiro."""
        if not self.autorizar_retiro(monto):
            return []

        pendiente = monto
        entregados = []
        for denominacion in sorted(self.billetes, reverse=True):
            cantidad, pendiente = divmod(pendiente, denominacion)
            entregados.extend([denominacion] * cantidad)

        if pendiente:
            raise ValueError("No se puede entregar el monto con las denominaciones disponibles.")

        self.actualizar_dinero(monto)
        return entregados
