# Cajero Automático · Simulador ATM con Flet

Simulador interactivo de cajero automático (ATM) desarrollado en **Python** utilizando **Flet**. Proporciona una interfaz gráfica moderna inspirada en cajeros bancarios reales, con teclado numérico virtual, display digital, validación de retiros y un algoritmo probabilístico para la dispensación y visualización dinámica de billetes.

## Funciones disponibles

- **Teclado ATM interactivo:** Teclado numérico en pantalla (`0`-`9`, `BORRAR`, `ENTER`) con respuesta visual e interactiva.
- **Display digital:** Pantalla de alta visibilidad para visualizar e ingresar el monto solicitado en tiempo real.
- **Dispensación probabilística:** Algoritmo ponderado (`random.choices`) que asigna probabilidades a las diferentes denominaciones ($50, $100, $200, $500 y $1,000 MXN) de acuerdo con el rango del monto a retirar.
- **Visualización dinámica de billetes:** Representación gráfica en tarjetas estilizadas (`ft.Card`) ordenadas de mayor a menor denominación.
- **Reglas y validaciones de retiro:**
  - Monto mínimo de retiro: **$50 MXN**.
  - Monto máximo por transacción: **$6,000 MXN**.
  - Validación de múltiplos válidos ($100).
  - Verificación de fondos disponibles en el cajero (Fondo inicial: **$50,000 MXN**).
  - Notificaciones de estado en tiempo real (éxito en cian y errores o advertencias en rosa/magenta).

## Requisitos

- Python 3.10 o superior.
- `flet==0.85.3` (o la versión indicada en el `requirements.txt` del repositorio).

## Instalación

Desde la raíz del repositorio:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

Desde la carpeta `cajero`:

```bash
cd cajero
python3 app.py
```

O utilizando el CLI de Flet (con recarga en vivo):

```bash
flet run -r app.py
```

## Recorrido de demostración / Uso

1. **Ingresar un monto:** Utiliza el teclado numérico en pantalla para capturar la cantidad deseada (por ejemplo, `1500`).
2. **Corregir dígitos:** Presiona `BORRAR` para eliminar el último dígito tecleado.
3. **Confirmar transacción:** Presiona `ENTER`. La aplicación validará la solicitud:
   - Si la transacción es válida, se muestra el mensaje de confirmación (ej. `Retiro por $ 1500 exitoso`) y se despliegan las tarjetas de los billetes entregados.
   - Si el monto excede el máximo permitido ($6,000), no cumple el múltiplo correspondiente o supera los fondos del cajero, se notificará el motivo del error.
4. **Persistencia en sesión:** Cada retiro aprobado descuenta automáticamente el saldo total disponible en la bóveda del cajero.

## Arquitectura y Lógica

- `model.py`: Módulo de lógica de negocio y reglas del cajero.
  - Clase `Cajero`: administra el balance (`$50,000`), límite por transacción (`$6,000`) y catálogo de billetes (`[50, 100, 200, 500, 1000]`).
  - `calcular_pesos(monto)`: calcula la distribución de pesos estadísticos para cada denominación según el monto requerido.
  - `autorizar_retiro(monto)`: valida que el importe cumpla con las reglas operativas y fondos.
  - `mesaje_retiro(monto)`: genera el texto de retroalimentación y bandera de estado.
  - `entregar_dinero(monto)`: efectúa la selección probabilística de billetes y los entrega ordenados de forma descendente.
- `app.py`: Capa de presentación construida con Flet.
  - Ensambla la estructura del cajero (`maquina`), el display digital (`ventana`), los controles numéricos (`generarControles`), el indicador de `status` y la columna de tarjetas (`billetes`).

## Referencias

- [Documentación oficial de Flet](https://flet.dev/docs/)
- [Flet Card Control](https://flet.dev/docs/controls/card/)

