# Proyectos Flet

Fecha de creación: 25 de septiembre de 2026.

Repositorio con miniaplicaciones construidas en Python y Flet. Sirve como portafolio de práctica para interfaces gráficas, persistencia local, validación de datos y separación entre lógica de dominio y capa visual.

## Contenido

- `suma-binaria/`: demo simple para sumar dos números binarios desde una interfaz Flet.
- `sudoku/` : demo simple de un sudoku 3x3 con GUI Flet.
- `finanzas/` : demo simple de seguidor de gastos GUI Flet + persistencia local.
- `files-manager/`: gestor local para explorar carpetas, crear directorios y
  eliminar archivos o carpetas con confirmación.
- `tabla-periodica/`: explorador interactivo de los 118 elementos, con
  configuración electrónica, electrones de valencia y análisis básico de
  dopaje y materiales.
- `newton/`: visualizador del método de Newton para funciones de dos variables,
  con registro de iteraciones y superficie 3D.
- `cards/`: generador visual de tarjetas de presentación/perfiles de usuario aleatorios usando Faker y Flet.

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
python3 files-manager/app.py
```

El gestor de archivos inicia en la carpeta personal del usuario. Usa los
controles de ubicación para entrar a carpetas o subir un nivel; **Nueva
carpeta** crea directorios y el botón de eliminar pide confirmación antes de
borrar el elemento seleccionado.

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

## Cards

Generador de tarjetas de perfil con avatares aleatorios. Requiere `faker` además de Flet:

```bash
cd cards
python3 -m pip install faker
python3 main.py
```

Consulta [`cards/README.md`](file:///Users/romero/escuela/pythonP/fleting/proyectos/cards/README.md) para más detalles y oportunidades de colaboración.
