# Recetario Personal 🍳

Aplicación de escritorio para gestionar recetas, ingredientes y pasos de preparación, construida con Python, **Flet 1.0** y MySQL.

## Características

- Crear, consultar, editar y eliminar recetas.
- Agregar ingredientes con cantidad y unidad (el catálogo reutiliza los ingredientes por nombre) y pasos ordenados.
- Buscar recetas por título.
- Errores de validación y de base de datos mostrados en la propia interfaz: dentro del diálogo, en un aviso o en una pantalla con **Reintentar** si MySQL no responde.
- Interfaz, servicios, repositorios y dominio separados; la lógica se prueba sin MySQL ni ventana.

## Requisitos

- Python 3.10 o superior.
- MySQL disponible en el host indicado en `.env`.
- `flet==1.0.3`, `mysql-connector-python`, `pydantic` y `python-dotenv` (ver `requirements.txt`).

## Instalación y configuración

Desde la raíz del repositorio:

```bash
cd recetario
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Edita `.env` con los datos de conexión a MySQL (`RECETARIO_DB_HOST`, `_PORT`, `_USER`, `_PASSWORD`, `_NAME`). El archivo `.env` está ignorado por Git; no agregues contraseñas al repositorio.

Crea la base de datos y carga el esquema incluido en [`schema.sql`](schema.sql):

```sql
CREATE DATABASE coocking;
USE coocking;
```

Ejecuta después el contenido de `schema.sql` en esa base de datos.

## Ejecución

Desde la carpeta `recetario`, con el entorno virtual activado:

```bash
python3 main.py
# o, con recarga en vivo:
flet run -r
```

## Pruebas

Desde la carpeta `recetario`. Los repositorios y la conexión se simulan, así que no se necesita MySQL:

```bash
python3 -m unittest discover -s tests -t . -v
```

## Estructura

```text
recetario/
├── main.py            # Punto de entrada: configura la ventana y llama a page.render(App, servicio)
├── ui/                # Interfaz declarativa (componentes y hooks de Flet)
│   ├── app.py         # App: estado, carga de datos, acciones y diálogos abiertos
│   ├── sidebar.py     # Buscador y lista de recetas
│   ├── detail.py      # Detalle: encabezado, ingredientes y pasos
│   ├── dialogs.py     # Diálogos de captura y confirmación
│   ├── widgets.py     # Toast, tarjeta de sección, contador, aviso vacío
│   └── theme.py       # Colores y medidas
├── services/          # RecipeService: validación y casos de uso
├── repositories/      # Una clase por tabla; solo SQL y mapeo a modelos
├── domain/            # Modelos pydantic: Recipe, RecipeDetail, Ingredient, Instruction…
├── database/          # Conexión (config.py) y consultas (query.py, StorageError)
├── tests/
├── schema.sql         # Esquema de las tablas
├── requirements.txt
└── .env.example       # Plantilla de configuración local
```

### Capas

- **`database`**: abre una conexión por consulta y traduce los errores del driver a `StorageError`. Expone `fetch_all`, `fetch_one` y `execute`.
- **`repositories`**: cada método es una consulta y devuelve modelos tipados (`Recipe`, `IngredientLine`…).
- **`services.RecipeService`**: recibe sus repositorios en el constructor (`create_service()` arma los de MySQL), normaliza y valida los textos y lanza `ValueError` con mensajes aptos para el usuario.
- **`ui`**: solo conoce el servicio; no hay SQL ni acceso a la base.

### Interfaz declarativa

- `App(service)` guarda el estado con `ft.use_state` (recetario cargado, selección, búsqueda, diálogo abierto y aviso) y deriva el resto: la receta seleccionada, la lista filtrada y el detalle (`ft.use_memo`, que se recalcula al subir `revision` tras cada cambio).
- Los diálogos y el aviso son componentes que usan `ft.use_dialog`: se muestran mientras están montados y desaparecen al desmontarse. Si el formulario falla (`ValueError`/`StorageError`), el mensaje aparece en el diálogo y este sigue abierto.
- `page.render(App, create_service())` monta la aplicación.

## Cambios de la migración a Flet 1.0.3

- UI declarativa con `@ft.component`, `ft.use_state`, `ft.use_memo`, `ft.use_dialog` y `page.render`, en lugar de funciones anidadas que mutan controles.
- El punto de entrada es `main.py` (antes `app.py`).
- Los repositorios y el servicio pasaron de métodos estáticos con nombres en camelCase a clases con métodos en `snake_case` y devuelven modelos en lugar de diccionarios.
- Se eliminó el código sin uso (actualizar/borrar ingredientes del catálogo, actualizar cantidades y pasos, listar el catálogo).
- Un número de paso inválido ahora se avisa en el diálogo; antes se sustituía en silencio por el siguiente número.
