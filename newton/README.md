# Newton Optimizer & Surface Visualizer

Aplicación de Flet que aplica el método de Newton a una función simbólica de dos variables, muestra sus iteraciones y dibuja la superficie 3D con la trayectoria calculada.

## Ejecutar

```bash
cd newton
python3 -m pip install -r requirements.txt
python3 app.py
```

## Uso

Escribe una expresión de SymPy con exactamente dos variables y un punto inicial separado por coma. Por ejemplo: `(x-2)**4 + (x-2*y)**2` y `0, 0`.

El método localiza puntos estacionarios; estos no siempre son mínimos. Al converger, la app clasifica el resultado como mínimo local, máximo local o punto silla/plano según la Hessiana.

## Estructura

- `optimizer.py`: análisis simbólico, iteraciones de Newton y clasificación Hessiana.
- `app.py`: interfaz Flet y representación 3D.
- `test_optimizer.py`: pruebas de las clasificaciones de puntos estacionarios.
