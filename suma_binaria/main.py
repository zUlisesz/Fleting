import flet as ft

def algoritmo_uno( primero :str, segundo: str) -> str:
    
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

def main(page: ft.Page)-> None:
    page.title = 'Suma de números binarios'

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    entrada_1 = ft.TextField( label = 'Primer número')
    entrada_2 = ft.TextField( label = 'Segundo número')


    salida = ft.Text( value= 'Ingresa tus dos números (en binario) y presiona el botón')

    def sumar( e):
        salida.value = f'Suma total: {algoritmo_uno(entrada_1.value, entrada_2. value)}'
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
                    content= ft.Text('Sumar'), 
                    on_click= sumar
                )
            ]
        )
    )

ft.run(main)