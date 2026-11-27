# Cards · Perfiles de Usuario

Visualizador de tarjetas de usuario generado con **Flet** y **Faker**, mostrando nombres, números telefónicos, direcciones y avatares personalizados.

## Requisitos

- Python 3.10+
- `flet==1.0.3`
- `faker`

Instalación de dependencias (el `requirements.txt` de la raíz solo fija Flet; este añade `faker`):
```bash
pip install -r requirements.txt
```

## Ejecución

Desde el directorio `cards`:

```bash
python3 main.py
```

o mediante el CLI de Flet:

```bash
flet run main.py
```

## Estructura

- `main.py`: interfaz declarativa de Flet 1.0 con componentes y hooks.
  - `UserCard(user)`: tarjeta de un perfil.
  - `Toolbar(...)`: slider de cantidad (1–12) y botón para regenerar.
  - `App()`: componente raíz con el estado.
- `model.py`: generación de datos falsos (`User`, `generate_users`, `make_user`), sin dependencias de Flet. Ya no se generan datos al importar el módulo.
- `assets/`: avatares masculinos y femeninos (`man_1..6`, `woman_1..6`).

## Estilo declarativo (Flet 1.0)

La UI se describe como función del estado, en lugar de mutar controles y llamar a `page.update()`:

- `@ft.component` convierte una función en componente reutilizable que se re-renderiza al cambiar su estado o sus argumentos.
- `ft.use_state` guarda la cantidad de perfiles y un contador de versión; los setters disparan el nuevo render.
- `ft.use_memo(..., [cantidad, version])` evita regenerar perfiles en renders que no cambian esas dependencias.
- `page.render(App)` monta el componente raíz; `ft.run(main, assets_dir="assets")` inicia la app.

## Asignación de avatares

El generador baraja los doce avatares disponibles y los asigna sin repetición durante cada ciclo. Si se solicitan más de doce perfiles, inicia un ciclo nuevo, por lo que los avatares solo se repiten después de que todos se hayan usado una vez.

`generate_users()` acepta una semilla opcional para producir el mismo conjunto de perfiles durante demostraciones o pruebas, por ejemplo `generate_users(5, seed=7)`.
