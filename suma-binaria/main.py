import flet as ft

def suma( primero :str, segundo: str) -> str:

    if not bin_valid(primero) or not bin_valid(segundo):
        return 'TYPE VALID BINARY NUMBERS'

    
    c = pasar_binario(primero) + pasar_binario( segundo)
    lista = []
    i = 0
    suma, max = 0 , 0
    
    while True:
        if 2 ** i > c :
            max = i -1
            break
        i+=1

    for i in range(max , -1, -1 ):
        if c - (2 ** i) >= 0:
            suma += ( 2 ** i)
            c -= ( 2 ** i)
            lista.append('1')
        else:
            lista.append('0')

    return ''.join( lista)

def pasar_binario( n) -> int:
    contador = 0
    longitud = len(n) -1
    for i in range(longitud +1) :
        
        if n[i] == '1':
            contador += 2 ** (longitud -i)

    return contador

def bin_valid( n : str) -> bool :
    for character in n:
        if character not in ['0', '1']: return False

    return True


def main(page: ft.Page)-> None:
    page.title = 'BINARY NUMBERS ADDITION'

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    entrada_1 = ft.TextField( label = 'TYPE YOUR FIRST BINARY')
    entrada_2 = ft.TextField( label = 'TYPE YOUR FIRST BINARY')


    salida = ft.Text( value= 'RESULT WILL APPEAR HERE :)')

    def sumar(e):
        salida.value = f'RESULT : {suma(entrada_1.value, entrada_2. value)}'
        page.update() 

    page.add(
        ft.Column(
            spacing= 20,
            controls= [
                entrada_1, 
                entrada_2,
                salida,
                ft.Button(
                    elevation= 10 ,
                    content= ft.Text('ADD'), 
                    on_click= sumar
                )
            ]
        )
    )

ft.run(main)