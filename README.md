# Proyectos Flet

Fecha de creación: 25 de septiembre de 2026.

Repositorio con miniaplicaciones construidas en Python y Flet. Sirve como portafolio de práctica para interfaces gráficas, persistencia local, validación de datos y separación entre lógica de dominio y capa visual.

## Contenido

- `suma-binaria/`: demo simple para sumar dos números binarios desde una interfaz Flet.
- `sudoku/` : demo simple de un sudoku 3x3 con GUI Flet.
- `finanzas/` : demo simple de seguidor de gastos GUI Flet + persistencia local.
- `tabla-periodica/`: explorador interactivo de los 118 elementos, con
  configuración electrónica, electrones de valencia y análisis básico de
  dopaje y materiales.
- `newton/`: visualizador del método de Newton para funciones de dos variables,
  con registro de iteraciones y superficie 3D.

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

## Tabla periódica

`tabla-periodica` se instala y ejecuta de forma independiente porque declara
sus propias dependencias de Flet. Desde la raíz del repositorio:

```bash
cd tabla-periodica
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
flet run src/main.py
```

Para abrirla en el navegador, sustituye el último comando por:

```bash
flet run --web src/main.py
```

Dentro de la aplicación se puede buscar un elemento por nombre o símbolo,
consultar sus propiedades y analizar pares como `Si` y `P` en el panel de
**Dopaje y Materiales**. Consulta `tabla-periodica/README.md` para la
verificación, estructura y opciones de empaquetado.

## Visualizador de Newton

El proyecto `newton` usa la misma versión de Flet del repositorio (`0.85.3`) y
además requiere NumPy, SymPy y Matplotlib. Desde la raíz del repositorio:

```bash
python3 -m venv .venv-newton
source .venv-newton/bin/activate
python -m pip install -r newton/requirements.txt
python -m newton.app
```

Escribe una función con exactamente dos variables, por ejemplo
`(x-2)**4 + (x-2*y)**2`, y un punto inicial como `0, 0`. La aplicación muestra
las iteraciones de Newton y la trayectoria sobre la superficie generada.

Si quieres conocer más sobre el método revisa el libro [Vector Calculus](https://www.mecmath.net/VectorCalculus.pdf) página 89.
