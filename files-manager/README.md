# Gestor de archivos

Aplicación local de Flet 1.0 para explorar una carpeta, buscar elementos por nombre, crear subcarpetas, renombrar y eliminar con confirmación. La interfaz es declarativa (`@ft.component`, `ft.use_state`, `ft.use_memo`, `ft.use_dialog`) y se monta con `page.render(App)`.

## Ejecutar

```bash
pip install -r requirements.txt
python3 main.py        # o: flet run main.py    # o: flet run
```

## Buscador

El campo «Buscar en esta carpeta» filtra por nombre (sin distinguir mayúsculas) **solo entre los elementos de la carpeta actual**:

- Encuentra archivos y carpetas que estén directamente en la carpeta que ves.
- **No** encuentra elementos dentro de subcarpetas, ni en carpetas hermanas o superiores.
- Al entrar a otra carpeta o subir un nivel, la búsqueda se limpia porque su alcance cambia.
- Los elementos ocultos (nombres que empiezan con `.`) no se listan ni se buscan.

La lógica está en `Shell.search()` (`shell.py`) y está cubierta por `tests/test_shell.py`.

## Alcance de seguridad

La carpeta inicial es el límite de navegación de la sesión. La aplicación permite entrar a subcarpetas y volver a sus niveles superiores dentro de ese límite, pero no salir de él. Al llegar a la carpeta inicial, el botón para subir se deshabilita. Las eliminaciones son permanentes y se solicitan con confirmación.

## Estructura

- `main.py`: componente `App` (estado y acciones) y punto de entrada.
- `ui.py`: componentes de presentación (`Header`, `LocationBar`, `SearchBar`, `EntryRow`, diálogos y aviso).
- `shell.py`: navegación, búsqueda y operaciones de archivos acotadas a la carpeta inicial; no depende de Flet.
- `tests/`: pruebas de `shell.py` y de renderizado (`render.py` expande componentes sin abrir ventana).

## Pruebas

```bash
python3 -m unittest discover -s tests -t .
```

Los diálogos usan `ft.use_dialog`, que requiere una página real; esa parte no se ejercita en las pruebas.
