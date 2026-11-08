# Sudoku

Juego de Sudoku construido con Flet. Genera una solución válida, oculta casillas para formar el tablero y registra intentos, tiempo y estado de la partida.

## Ejecutar

```bash
cd sudoku
python3 main.py
```

## Controles

Selecciona una casilla vacía y usa el teclado numérico para colocar un valor. Las pistas no se pueden modificar y, al tocarlas, se conserva la última casilla editable seleccionada. La partida finaliza al completar la solución o al agotar los intentos.

## Pruebas

```bash
python3 -m unittest sudoku.tests.test_algoritmo -v
```

## Estructura

- `algoritmo.py`: generación y reglas de la partida.
- `main.py`: interfaz Flet.
- `tests/test_algoritmo.py`: pruebas de selección y jugabilidad.
