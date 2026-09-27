# Tabla Periódica e Ingeniería de Materiales

Aplicación interactiva construida con Flet para explorar los 118 elementos de
la tabla periódica y relacionar sus electrones de valencia con casos básicos de
materiales y dopaje.

## Funciones disponibles

- Visualización de la tabla periódica organizada por categorías de elementos.
- Búsqueda por símbolo o nombre; los elementos coincidentes se resaltan.
- Consulta de número atómico, masa, categoría, configuración electrónica,
  electrones de valencia y huecos de un elemento.
- Análisis de dos símbolos químicos para clasificar combinaciones básicas como
  semiconductor intrínseco, dopaje tipo N, dopaje tipo P, conductor o aislante.

## Requisitos

- Python 3.10 o superior.
- Dependencias declaradas en `requirements.txt` (`flet==0.86.5` y paquetes de
  ejecución, compilación y pruebas de Flet).

El repositorio raíz tiene sus propias dependencias y una versión distinta de
Flet. Instala las de este proyecto antes de ejecutarlo.

## Instalación

Desde la carpeta `tabla-periodica`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Ejecución

Con el entorno virtual activado, ejecuta la aplicación de escritorio:

```bash
flet run src/main.py
```

Para iniciarla como aplicación web:

```bash
flet run --web src/main.py
```

## Uso

1. Escribe un símbolo o nombre en **Buscar elemento...** para ubicarlo en la
   tabla.
2. Haz clic en una celda para mostrar sus propiedades químicas.
3. En **Dopaje y Materiales**, captura dos símbolos válidos, por ejemplo `Si`
   y `P`, y selecciona **Analizar Unión**.

## Verificación

Desde la carpeta del proyecto:

```bash
python -m py_compile src/main.py src/algorithm.py
flet test macos .
```

La primera ejecución de las pruebas de integración puede descargar los
componentes de Flutter requeridos por Flet.

## Estructura principal

- `src/main.py`: interfaz, búsqueda, detalle de elementos y análisis de
  combinaciones.
- `src/algorithm.py`: cálculo de configuración electrónica, valencia y huecos.
- `src/elements.json`: datos de los 118 elementos.
- `src/table.json`: distribución visual de la tabla.
- `src/colors.json`: colores por categoría.
- `tests/test_main.py`: prueba de integración de la pantalla principal.

## Empaquetado

Flet permite crear distribuciones para plataformas específicas desde esta
carpeta. Por ejemplo:

```bash
flet build web
flet build macos
flet build apk
```

Consulta la documentación oficial de Flet para los requisitos de firma y
publicación de cada plataforma.
