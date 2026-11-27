# Enfoque · Organizador personal

Fecha de creación: 19 de septiembre de 2026.

Lista de tareas con título, prioridad y estado; alta y edición; búsqueda por texto; filtros por estado; resumen global con barra de progreso; modo claro/oscuro; borrado con confirmación y persistencia en SQLite. Es un proyecto de **UI imperativa** con Flet 1.0: los controles se crean una vez y los manejadores los modifican y llaman a `page.update()` (ver el [README principal](../README.md#declarativo-frente-a-imperativo)).

## Requisitos

- Python 3.10 o superior.
- `flet==1.0.3` (ver `requirements.txt`).

## Ejecución

Desde la carpeta que contiene `organizador/` (la raíz del repositorio):

```bash
python3 -m pip install -r organizador/requirements.txt
python3 -m organizador.main
```

El módulo usa un import relativo (`from .modelo import ...`), por eso se ejecuta como paquete con `-m`.

## Recorrido de demostración

1. Intenta agregar un título vacío: aparece un error junto al campo.
2. Agrega «Preparar exposición» con prioridad Alta y «Leer capítulo» con Media.
3. Marca la primera como completada: total 2, pendientes 1, completadas 1.
4. Busca «capítulo»; el resumen sigue siendo global y la lista muestra una tarea.
5. Limpia la búsqueda y usa Editar; el formulario superior cambia a «Guardar cambios».
6. Cancela una eliminación y verifica que el registro sigue presente.
7. Cierra y vuelve a abrir: las tareas conservan sus estados.

## Pruebas

Desde la raíz del repositorio:

```bash
python3 -m unittest discover -s organizador/tests -t . -v
```

- `tests/test_modelo.py`: validación, persistencia en una base temporal, orden, búsqueda, filtros, ids inexistentes y restricciones de la base.
- `tests/test_main.py`: construye la interfaz con una página simulada y comprueba el formulario, el error de título vacío y el cambio de tema. No abre ninguna ventana.

## Arquitectura

- `modelo.py`: dataclass `Tarea`, validación y repositorio SQLite, sin dependencias de Flet. Consultas parametrizadas y una conexión por operación.
- `main.py`: controles, manejadores, formulario, confirmación y representación del estado.
- `tests/`: pruebas de ambos módulos.

Flujo: evento → validación → escritura en el repositorio → recarga → actualización de controles. Las tareas se identifican por id, no por posición, y el formulario recuerda el id durante una edición.

La base se crea vacía en `~/.flet_curso/organizador.sqlite3`; la variable de entorno `FLET_CURSO_DATA_DIR` permite cambiar el directorio.

## Alcance

Pensada para una persona y un volumen pequeño de tareas. No incluye autenticación, sincronización entre sesiones ni migraciones de esquema. El modo oscuro es una preferencia de sesión. Si el almacenamiento no se puede abrir, la app muestra el motivo en pantalla.

## Extensión sugerida

Agregar una fecha límite sin mezclar SQL dentro de los manejadores: primero la validación, el filtro y sus pruebas en `modelo.py`.

Referencia: [controles oficiales de Flet](https://flet.dev/docs/controls/).
