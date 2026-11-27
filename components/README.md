# Components · Catálogo de componentes Flet

Biblioteca de componentes reutilizables para Flet 1.0.3 (átomos estilo shadcn/ui) y un catálogo navegable de ejemplos: botones, inputs, contenedores, tarjetas, tablas, gradientes, shimmer, colores e iconos.

Todo está escrito de forma **declarativa**: componentes con `@ft.component`, estado con hooks (`ft.use_state`, `ft.use_memo`) y montaje con `page.render(...)`.

## Instalación y ejecución

```bash
pip install -r requirements.txt
```

Desde esta carpeta:

```bash
python3 main.py        # o: flet run main.py
```

Desde la carpeta que contiene `components/`:

```bash
python3 -m components.main
```

## Estructura

```
components/
├── main.py        # punto de entrada (page.render(App))
├── app.py         # App: barra lateral + galería seleccionada
├── theme.py       # tokens de color (COLORS)
├── atoms/         # componentes reutilizables
└── gallery/       # catálogo de ejemplos (una página por archivo)
```

## Usar los componentes

Los átomos viven en `components.atoms`. Son componentes declarativos: llámalos **dentro de otro componente** y monta la raíz con `page.render`.

```python
import flet as ft
from components.atoms import Button, IconButton, SearchInput, Surface, TextInput


@ft.component
def Formulario() -> ft.Control:
    nombre, set_nombre = ft.use_state("")
    guardado, set_guardado = ft.use_state(False)

    return Surface(
        ft.Column(
            [
                TextInput("Nombre", value=nombre, on_change=lambda e: set_nombre(e.control.value)),
                Button("Guardar", icon=ft.Icons.SAVE, on_click=lambda _: set_guardado(True)),
                ft.Text("Guardado" if guardado else ""),
            ]
        )
    )


ft.run(lambda page: page.render(Formulario))
```

### Referencia

| Componente | Parámetros principales |
| --- | --- |
| `Button(label, *, variant="default", icon, on_click, disabled)` | `variant`: `"default"` (relleno) u `"outline"` (contorno). |
| `IconButton(icon, *, on_click, tooltip, selected, size=44, icon_size=22, inverse=False)` | `inverse=True` lo muestra oscuro. |
| `TextInput(label="", *, value, hint_text, password, can_reveal_password, outlined, prefix_icon, on_change, width=320)` | Controlado: guarda `value` con `ft.use_state`. |
| `SearchInput(*, value, hint_text="Search", on_change, width=360)` | `TextInput` con icono de lupa. |
| `Surface(content, *, padding=24, radius=14, bgcolor, width, height)` | Agrupa contenido con borde y esquinas redondeadas. |

Los colores salen de `components.theme.COLORS`; cámbialos ahí para retematizar todos los átomos.

### Reglas al crear componentes

- Un componente se llama como función y puede recibir `key=` para identificarlo en listas: `Button("Ok", key="ok")`.
- Si lo colocas dentro de un `ft.ResponsiveRow`, envuélvelo en un `ft.Container(col=...)`. Para evitarlo usa `ResponsiveGrid` de `components.gallery._layout`.
- Los hooks solo se llaman dentro de un componente.

## Catálogo (galerías)

Cada página del catálogo es un componente en `gallery/` y se registra en `gallery/__init__.py` (`SECTIONS`). Para añadir una:

1. Crea `gallery/mi_pagina.py` con un `@ft.component` que devuelva un control.
2. Añade `Section("clave", "Título", "Descripción", ft.Icons.ALGO, MiPagina)` a `SECTIONS`.

Helpers compartidos: `ResponsiveGrid` y `sample_grid` (`gallery/_layout.py`) y `CatalogBrowser` (`gallery/_catalog.py`), un explorador con búsqueda y paginación para catálogos grandes.

## Pruebas

Desde la carpeta que contiene `components/`:

```bash
python3 -m unittest discover -s components/tests -t . -v
```

`tests/render.py` expande un árbol de componentes sin abrir una ventana, útil para probar los tuyos.
