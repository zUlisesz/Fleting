# Cajero Automático · Simulador ATM con Flet

Simulador interactivo de cajero automático (ATM) desarrollado en **Python** utilizando **Flet**. Proporciona una interfaz gráfica moderna inspirada en cajeros bancarios reales, con teclado numérico virtual, display digital, validación de retiros y dispensación exacta de billetes.

## Funciones disponibles

- **Teclado ATM interactivo:** Teclado numérico en pantalla (`0`-`9`, `BORRAR`, `ENTER`) con respuesta visual e interactiva.
- **Display digital:** Pantalla de alta visibilidad para visualizar e ingresar el monto solicitado en tiempo real.
- **Dispensación exacta:** El cajero usa las denominaciones disponibles ($50, $100, $200, $500 y $1,000 MXN) de mayor a menor, asegurando que los billetes entregados sumen exactamente el monto autorizado.
- **Visualización dinámica de billetes:** Representación gráfica en tarjetas estilizadas (`ft.Card`) ordenadas de mayor a menor denominación.
- **Reglas y validaciones de retiro:**
  - Monto mínimo de retiro: **$100 MXN**.
  - Monto máximo por transacción: **$6,000 MXN**.
  - Validación de múltiplos válidos ($100).
  - Verificación de fondos disponibles en el cajero (Fondo inicial: **$50,000 MXN**).
  - Notificaciones de estado en tiempo real (éxito en cian y errores o advertencias en rosa/magenta).

## Requisitos

- Python 3.10 o superior.
- `flet==1.0.3` y `flet-audio==1.0.3` (ver `cajero/requirements.txt`).

## Instalación

Desde la raíz del repositorio:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r cajero/requirements.txt
```

> `cajero` también usa `flet-audio`, que no está en el `requirements.txt` de la raíz; instala el de `cajero/`.

## Ejecución

Desde la carpeta `cajero`:

```bash
cd cajero
python3 main.py
```

O utilizando el CLI de Flet (con recarga en vivo):

```bash
flet run -r main.py
```

## Recorrido de demostración / Uso

1. **Ingresar un monto:** Utiliza el teclado numérico en pantalla para capturar la cantidad deseada (por ejemplo, `1500`).
2. **Corregir dígitos:** Presiona `BORRAR` para eliminar el último dígito tecleado.
3. **Confirmar transacción:** Presiona `ENTER`. La aplicación validará la solicitud:
   - Si la transacción es válida, se muestra el mensaje de confirmación (ej. `Retiro por $ 1500 exitoso`) y se despliegan las tarjetas de los billetes entregados.
   - Si el monto excede el máximo permitido ($6,000), no cumple el múltiplo correspondiente o supera los fondos del cajero, se notificará el motivo del error.
4. **Persistencia en sesión:** Cada retiro aprobado descuenta automáticamente el saldo total disponible en la bóveda del cajero.

## Pruebas

Desde la raíz del repositorio, ejecuta las pruebas de reglas y saldo del cajero:

```bash
python3 -m unittest discover -s cajero/tests -t . -v
```

## Arquitectura y Lógica

- `model.py`: lógica de negocio, sin dependencias de Flet.
  - Constantes del dominio (`SALDO_INICIAL`, `MONTO_MINIMO`, `MONTO_MAXIMO`, `MULTIPLO`, `DENOMINACIONES`).
  - `Cajero` (dataclass): administra el saldo y el límite por transacción.
  - `autorizar_retiro(monto)` y `mensaje_retiro(monto)` comparten una única validación (`_error_retiro`), por lo que nunca se contradicen.
  - `entregar_dinero(monto)`: entrega billetes exactos de mayor a menor y descuenta el saldo.
- `main.py`: interfaz con Flet 1.0.
  - `CajeroView`: concentra estado, eventos y construcción de la UI (sin variables compartidas por cierre).
  - `billete_card` y `boton`: constructores de controles reutilizables.
  - Teclado con `ft.Button`, límite de 5 dígitos y sonidos con `flet_audio.Audio`.

## Migración a Flet 1.0.3

- `Audio` es un `ft.Service`: se registra en `page.services` (ya no en `page.overlay`) y sus métodos (`play()`) son corrutinas.
- Se usa `ft.run(main, assets_dir="assets")` en lugar de `ft.app`.
- Alineaciones y bordes con la API vigente: `ft.Alignment.CENTER`, `ft.Border.all`, `ft.Padding.symmetric`.
- Teclas con `ft.Button` + `ft.ButtonStyle` (accesibles) en lugar de `ft.Container` con `on_click`.
- El punto de entrada pasó de `app.py` a `main.py`.

## Referencias

- [Documentación oficial de Flet](https://flet.dev/docs/)
- [Flet Card Control](https://flet.dev/docs/controls/card/)

