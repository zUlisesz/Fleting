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

## Invitación a Colaborar / Open Contribution
### Mejora pendiente: Algoritmo de asignación de avatares únicos
Actualmente, la función `get_random_avatar(gender)` en `model.py` selecciona un avatar de manera aleatoria (`random.randint(1, 6)`), lo que puede provocar que **se repitan avatares** entre las tarjetas generadas en pantalla.

Buscamos aportaciones y propuestas de mejora, tales como:
- Implementar un algoritmo que evite la repetición de avatares (por ejemplo, barajado/muestreo sin reemplazo o un pool de avatares disponibles).
- Manejo inteligente del pool cuando el número de usuarios supere los avatares disponibles.
- Incorporación de nuevos avatares o categorías.

Si deseas contribuir, siéntete libre de abrir un Pull Request o proponer mejoras en la lógica de asignación.
