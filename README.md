# Proyectos Flet

Fecha de creación: 25 de septiembre de 2026.

Repositorio con miniaplicaciones construidas en Python y Flet. Sirve como portafolio de práctica para interfaces gráficas, persistencia local, validación de datos y separación entre lógica de dominio y capa visual.

## Contenido

- `suma-binaria/`: demo simple para sumar dos números binarios desde una interfaz Flet.
- `sudoku/` : demo simple de un sudoku 3x3 con GUI Flet.
- `finanzas/` : demo simple de seguidor de gastos GUI Flet + persistencia local.

## Instalación

Desde esta carpeta:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Ejecución

Cada proyecto puede ejecutarse de forma independiente:

```bash
python3 -m suma-binaria.main
python3 -m sudoku.main
python3 -m finanzas.app
```

