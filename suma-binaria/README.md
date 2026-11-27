# Suma binaria

Suma dos números binarios y muestra la operación "en papel": los acarreos de cada columna, los sumandos alineados, la línea y el resultado, junto con su equivalente en decimal. Construida con **Flet 1.0** y UI declarativa.

## Uso

Escribe dos números en los campos (solo aceptan `0` y `1`, hasta 16 bits). El resultado se calcula mientras escribes; **Limpiar** vacía ambos campos.

| Primer número | Segundo número | Resultado | Decimal |
| ------------- | -------------- | --------- | ------- |
| `101`         | `11`           | `1000`    | 5 + 3 = 8 |

## Ejecución

```bash
python3 -m pip install -r requirements.txt
python3 main.py        # o: flet run
```

## Pruebas

Desde esta carpeta:

```bash
python3 -m unittest discover -s tests -t . -v
```

## Estructura

- `binario.py`: lógica pura (`es_binario`, `sumar`, `Suma`), sin Flet. `sumar` lanza `ValueError` con un mensaje si la entrada no es válida.
- `main.py`: componentes `App`, `BinaryField`, `AdditionSheet`, `BitRow`, `CarryRow`, `Bit`, `Equivalence` y `Placeholder`.
- `tests/`: pruebas de la lógica (incluye una comparación contra la suma de enteros) y de los componentes.

## Cómo está hecha

- `App` guarda solo los dos textos con `ft.use_state`. El resultado se **deriva** de ellos con `ft.use_memo`; no hay botón "Sumar" ni se asigna `salida.value`.
- El tamaño de las casillas se calcula según el número de columnas para que la suma siempre quepa en la tarjeta.
- Cambios respecto a la versión anterior: el resultado es en vivo (antes había un botón **ADD**), los campos filtran lo que no sea `0`/`1`, y los errores de entrada se tratan con `ValueError` en lugar de devolver el texto `"TYPE VALID BINARY NUMBERS"`.
