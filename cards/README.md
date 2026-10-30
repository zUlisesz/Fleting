# Cards · Perfiles de Usuario

Visualizador de tarjetas de usuario generado con **Flet** y **Faker**, mostrando nombres, números telefónicos y avatares personalizados.

## Requisitos

- Python 3.10+
- `flet`
- `faker`

Instalación de dependencias:
```bash
pip install flet faker
```

## Ejecución

Desde el directorio `cards`:

```bash
cd cards
python3 main.py
```

o mediante el CLI de Flet:

```bash
flet run main.py
```

## Estructura

- `main.py`: Interfaz de usuario construida con Flet (tarjetas, layout y diseño visual).
- `model.py`: Generación de datos falsos (nombres, teléfonos, direcciones y asignación de avatares).
- `assets/`: Conjunto de imágenes de avatares masculinos y femeninos (`man_1..6`, `woman_1..6`).

## Asignación de avatares

El generador baraja los doce avatares disponibles y los asigna sin repetición durante cada ciclo. Si se solicitan más de doce perfiles, inicia un ciclo nuevo, por lo que los avatares solo se repiten después de que todos se hayan usado una vez.
