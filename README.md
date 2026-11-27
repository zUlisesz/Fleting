# Proyectos Flet

Fecha de creación: 25 de septiembre de 2026.

Repositorio con miniaplicaciones construidas en Python y **Flet**. Sirve como portafolio de práctica para interfaces gráficas, persistencia local, validación de datos y separación entre lógica de dominio y capa visual. Cada carpeta es un proyecto independiente con su propio `README.md`.

Además, el repositorio contiene a propósito **dos estilos de interfaz** (imperativo y declarativo) para poder compararlos: ver [Declarativo frente a imperativo](#declarativo-frente-a-imperativo).

## Proyectos

| Proyecto | Qué hace | Estilo | Flet |
| --- | --- | --- | --- |
| [`suma-binaria/`](suma-binaria/) | Suma dos binarios y dibuja la operación columna por columna. | declarativo | 1.0.3 |
| [`cards/`](cards/) | Tarjetas de perfil aleatorias (Faker). | declarativo | 1.0.3 |
| [`components/`](components/) | Biblioteca de componentes reutilizables (átomos y galería). | declarativo | 1.0.3 |
| [`files-manager/`](files-manager/) | Explorador de carpetas con búsqueda limitada a la carpeta actual. | declarativo | 1.0.3 |
| [`finanzas/`](finanzas/) | Ingresos y gastos por perfil, con SQLite. | declarativo | 1.0.3 |
| [`newton/`](newton/) | Método de Newton para funciones de dos variables, con superficie 3D. | declarativo | 1.0.3 |
| [`recetario/`](recetario/) | Recetas, ingredientes y pasos con MySQL. | declarativo | 1.0.3 |
| [`cajero/`](cajero/) | Cajero automático con teclado virtual y entrega exacta de billetes. | imperativo | 1.0.3 |
| [`organizador/`](organizador/) | Lista de tareas con búsqueda, filtros y SQLite. | imperativo | 1.0.3 |
| [`sudoku/`](sudoku/) | Sudoku 3×3 con intentos y temporizador. | imperativo | 1.0.3 |
| [`tabla-periodica/`](tabla-periodica/) | Los 118 elementos, configuración electrónica y dopaje. | imperativo | 1.0.3 |

> **Versiones.** Todos los proyectos usan `flet==1.0.3`. Cada uno declara sus dependencias en su propio `requirements.txt` (`tabla-periodica` además en `pyproject.toml`); el de la raíz solo fija Flet.

## Instalación

Todos los proyectos usan Flet 1.0.3 y algunos necesitan dependencias extra, así que instala el `requirements.txt` del proyecto que vayas a usar, preferiblemente en un entorno propio:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r <proyecto>/requirements.txt
```

## Ejecución

Desde la raíz del repositorio:

```bash
cd suma-binaria && python3 main.py
cd cards && python3 main.py
cd components && python3 main.py
cd files-manager && python3 main.py
cd recetario && python3 main.py             # requiere MySQL y .env, ver su README
cd cajero && python3 main.py
cd sudoku && python3 main.py
cd tabla-periodica && flet run src/main.py  # o: flet run --web src/main.py

python3 -m finanzas.main                    # estos dos usan imports relativos
python3 -m newton.main                      # y se ejecutan como paquete
python3 -m organizador.app
```

En los proyectos con `main.py` también sirve `flet run` (con `-r` para recarga en vivo).

## Pruebas

Cada proyecto documenta su comando en su README. Desde la raíz del repositorio:

```bash
python3 -m unittest discover -s cajero/tests -t .
python3 -m unittest discover -s components/tests -t .
python3 -m unittest discover -s finanzas/tests -t .
python3 -m unittest discover -s newton/tests -t .
python3 -m unittest discover -s organizador/tests -t .
python3 -m unittest cards.tests.test_main
python3 -m unittest sudoku.tests.test_algoritmo
(cd files-manager && python3 -m unittest discover -s tests -t .)
(cd recetario     && python3 -m unittest discover -s tests -t .)
(cd suma-binaria  && python3 -m unittest discover -s tests -t .)
(cd tabla-periodica && python3 -m pytest)   # requiere pytest; test_main.py usa flet[test]
```

Las pruebas de interfaz de los proyectos declarativos expanden los componentes en memoria (`tests/render.py`), sin abrir una ventana.

## Declarativo frente a imperativo

Flet permite construir la misma interfaz de dos maneras. Este repositorio tiene ambas.

### Imperativo: describes *cómo cambiar* la pantalla

Creas los controles una vez, guardas referencias a ellos y, cuando algo ocurre, **modificas** sus propiedades y avisas a Flet con `page.update()`.

```python
def main(page: ft.Page):
    count = ft.Text("0")

    def increment(e):
        count.value = str(int(count.value) + 1)   # mutas el control...
        page.update()                             # ...y pides que se redibuje

    page.add(count, ft.Button("+1", on_click=increment))

ft.run(main)
```

Ejemplos en el repositorio: `organizador` (la función `refrescar` reasigna `lista.controls` y llama a `page.update()`), `sudoku` (la clase `SudokuApp` guarda un diccionario de casillas y las recolorea), `tabla-periodica` y `cajero`.

### Declarativo: describes *cómo se ve* para un estado dado

El estado vive en hooks y los componentes son funciones que **devuelven** la interfaz que corresponde a ese estado. Al cambiarlo, Flet vuelve a ejecutar el componente y aplica solo las diferencias; no hay `page.update()` ni referencias a controles.

```python
@ft.component
def Counter():
    n, set_n = ft.use_state(0)
    return ft.Row([
        ft.Text(str(n)),
        ft.Button("+1", on_click=lambda _: set_n(n + 1)),
    ])

ft.run(lambda page: page.render(Counter))
```

Ejemplos: todos los demás; `suma-binaria` es el más corto y `recetario` el más completo.

### Diferencias principales

| | Imperativo | Declarativo |
| --- | --- | --- |
| **Fuente de verdad** | Los propios controles (`texto.value`, `lista.controls`). | Variables de estado (`ft.use_state`). La pantalla es una consecuencia. |
| **Actualizar la pantalla** | Tú: mutas controles y llamas a `page.update()`. | Flet: al cambiar el estado vuelve a ejecutar el componente. |
| **Valores derivados** | Hay que recalcularlos y asignarlos en cada manejador (fácil olvidarse de uno). | Se calculan al construir la vista (`ft.use_memo` si son costosos); nunca quedan desfasados. |
| **Estructura** | Una función `main` o una clase grande con muchos controles como atributos. | Muchos componentes pequeños que reciben datos y callbacks por parámetros. |
| **Reutilización** | Funciones que construyen controles; el estado queda disperso. | Un componente lleva su propio estado (`Dialog`, `BinaryField`) y se reutiliza con otros datos. |
| **Listas dinámicas** | Vaciar y volver a llenar `controls`. | Se devuelve la lista completa; `key=` identifica cada elemento. |
| **Diálogos y avisos** | `page.show_dialog(...)` / `page.pop_dialog()`. | Un componente con `ft.use_dialog`: se muestra mientras está montado. |
| **Pruebas** | Lógica aparte; la interfaz suele probarse a mano o con la ventana abierta. | Los componentes son funciones: se expanden en memoria y se inspeccionan sin ventana. |
| **Curva de aprendizaje** | Más directo al empezar; escala peor cuando hay mucho estado. | Pide pensar en estado e inmutabilidad; escala mejor. |

### Cuándo usar cada uno

- **Imperativo** cuando la pantalla es pequeña, el estado es mínimo o el control de bajo nivel importa (animaciones o actualizaciones muy puntuales de un solo control).
- **Declarativo** cuando hay varios estados que se combinan (filtros, selección, diálogos, errores) o cuando quieres componentes reutilizables y probables.

### Cosas que cambian al pasar a declarativo

- Un componente es un nodo diferido: **no tiene `col`, `expand`, etc.** Si lo pones en un `ResponsiveRow`, envuélvelo en `ft.Container(col=...)`.
- Los hooks se llaman siempre, en el mismo orden, en el cuerpo del componente (no dentro de `if` ni de bucles).
- Los estados se actualizan con el setter (`set_x(valor)` o `set_x(lambda actual: ...)`); no se muta el objeto guardado.
- Con listas de componentes, usa `key=` para que Flet conserve el estado de cada elemento.
- Un componente que usa `ft.use_dialog` necesita una página real; en pruebas se sustituye `flet.use_dialog` para capturar el diálogo.
- Los manejadores `async` se pasan directamente como `on_click`; si envuelves uno en un `lambda`, la corrutina no se espera.

## Convenciones del repositorio

- PEP 8; la lógica de dominio no importa Flet y vive en módulos propios (`model.py`, `dominio.py`, `services/`…), para probarla sin abrir una ventana.
- Pruebas con `unittest` (`pytest` solo en `tabla-periodica`), nombradas `test_*.py`.
- Commits con Conventional Commits y un cambio lógico por proyecto.
