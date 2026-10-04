import random
class Cajero:

    def __init__(self):
        self.dinero : int = 50_000
        self.max_monto : int = 6_000
        self.billetes = [50, 100, 200, 500, 1000]

    def actualizar_dinero(self, monto : int) :
        '''Actualiza el estado de cajero'''
        self.dinero -= monto

    @classmethod
    def calcular_pesos(cls, monto: int ) -> list[int]:
        if monto <= 500: return [3, 8, 6, 2, 0]
        if monto <= 1000: return [1,6,6,6,0]  
        if monto <= 2000: return [2,4,6, 8,2]
        if monto <= 300: return [2,4,4, 8,4]
        return [1, 2, 2, 4,10]

    def autorizar_retiro(self, monto: int ) -> bool:
        """Regrea un valor de True si se cumplen todas las condiciones\n
        de otra manera se regesa un valor False"""
        if monto > self.max_monto or monto < 50: return False
        if monto > self.dinero: return False
        if monto % 50 != 0 :return False
        return True
    
    def mesaje_retiro(self, monto : int ) :
        """
        Descripción\n
        :monto: int -> Recibe un número entero representando el monto a retirar\n
        :return: str -> 'Devuelve un mensaje de status sobre el intento de retiro
        """
        if monto > self.max_monto: return f'Monto máximo $ {self.max_monto}', False
        if monto < 50 : return 'Retiros mayores a $ 50', False
        if monto > self.dinero: return 'Saldo del cajero insuficiente', False
        if monto % 50!= 0 : return 'Monto inválido', False
        return f'Retiro por $ {monto} exitoso' , True

    def entregar_dinero( self, monto:  int) -> list[int ]:
        """Si se autoriza el retiro se devuelve una lista\n
        con los 'billetes' del retiro ordenados de mayor a menor"""
        
        if not self.autorizar_retiro(monto): return []
        weights = self.calcular_pesos(monto)

        billetes = []
        while monto >= 50 :
            r = random.choices( 
                self.billetes, 
                weights= weights,
                k= 1
            )[0]
            if r > monto : continue
            monto-= r
            billetes.append(r)

        self.actualizar_dinero( monto )
        return sorted(billetes, reverse= True)      