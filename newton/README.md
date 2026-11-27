# Newton Optimizer & Surface Visualizer

Aplicación de **Flet 1.0** que aplica el método de Newton a una función simbólica de dos variables, muestra cada iteración y dibuja la superficie 3D con la trayectoria calculada.

## Requisitos

- Python 3.10 o superior.
- `flet==1.0.3`, `matplotlib`, `numpy` y `sympy` (ver `requirements.txt`).

## Ejecución

Desde la carpeta que contiene `newton/` (la raíz del repositorio):

```bash
python3 -m pip install -r newton/requirements.txt
python3 -m newton.main
```

El módulo usa imports relativos (`from .analysis import ...`), por lo que se ejecuta como paquete con `-m`.

## Uso

1. Escribe una expresión de SymPy con **exactamente dos variables**, por ejemplo `(x-2)**4 + (x-2*y)**2`.
2. Escribe el punto inicial separado por coma, por ejemplo `0, 0`.
3. Pulsa **Optimizar** (o `Enter` en cualquiera de los campos).

La app muestra el registro de iteraciones, el estado del resultado y la gráfica. El método localiza puntos estacionarios, que no siempre son mínimos: al converger, el resultado se clasifica con la Hessiana como **mínimo local**, **máximo local** o **punto silla o plano**. Si no se cumple la tolerancia en 14 iteraciones, se muestra la trayectoria recorrida y se avisa que no hubo convergencia.

Los errores de entrada (función inválida, una sola variable, punto mal formado, Hessiana no invertible) se explican en el estado y no detienen la app.

> La función se interpreta con `sympy.sympify`, que evalúa el texto como una expresión de Python. Está pensada para uso local; no la expongas a entradas de terceros.

## Estructura

```text
newton/
├── optimizer.py   # Lógica pura: parseo, iteraciones de Newton y clasificación Hessiana
├── plotting.py    # Superficie y trayectoria como PNG en memoria (matplotlib)
├── analysis.py    # Caso de uso: optimizar + dibujar → Analysis (textos con tono e imagen)
├── main.py        # UI declarativa: componentes, hooks y page.render
└── tests/         # Pruebas de lógica, análisis, gráfica y componentes
```

`optimizer`, `plotting` y `analysis` no importan Flet, así que se prueban sin abrir una ventana.

### Interfaz declarativa

- Componentes: `Header`, `ProblemForm`, `LogPanel`, `ChartPanel` y `App`, todos con `@ft.component`.
- `App` guarda el estado con `ft.use_state` (función, punto inicial, resultado y si está calculando) y lo deriva en la vista; no hay controles guardados ni mutados.
- Al pulsar **Optimizar**, el cálculo y el dibujo se ejecutan con `asyncio.to_thread`, así que la ventana no se congela y el botón se deshabilita mientras tanto.
- `main(page)` configura la ventana y llama a `page.render(App)`.

## Pruebas

Desde la raíz del repositorio:

```bash
python3 -m unittest discover -s newton/tests -t . -v
```

## Migración a Flet 1.0.3

- UI declarativa (`@ft.component`, `ft.use_state`, `page.render`) en lugar de la clase `NewtonApp` con controles mutables.
- `main.py` es el punto de entrada (antes `app.py`) y desaparece el `try/except ImportError` de imports.
- Los componentes no admiten `col`: en `ResponsiveRow` se envuelven en `ft.Container(col=...)`.
