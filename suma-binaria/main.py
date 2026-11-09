import flet as ft

def suma(primero: str, segundo: str) -> str:
    if not bin_valid(primero) or not bin_valid(segundo):
        return "TYPE VALID BINARY NUMBERS"
    return format(pasar_binario(primero) + pasar_binario(segundo), "b")

def pasar_binario(n: str) -> int:
    return int(n, 2)

def bin_valid(n: str) -> bool:
    return bool(n) and all(character in "01" for character in n)

def main(page: ft.Page)-> None:
    page.title = 'BINARY NUMBERS ADDITION'
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.alignment = ft.Alignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    entrada_1 = ft.TextField( label = 'TYPE YOUR FIRST BINARY')
    entrada_2 = ft.TextField( label = 'TYPE YOUR SECOND BINARY')

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
                    width= 300,
                    height= 40,
                    content= ft.Text('ADD'), 
                    on_click= sumar
                )
            ]
        )
    )

if __name__ == "__main__":
    ft.run(main)
