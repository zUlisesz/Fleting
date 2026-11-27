# Balance · Flujo de efectivo personal

Demostración de Flet 1.0 para registrar ingresos y gastos en MXN, consultar el saldo, filtrar por categoría, tipo y mes, comparar categorías con barras y eliminar registros con confirmación. Almacenamiento SQLite local con importes en centavos enteros. La interfaz es declarativa (`@ft.component`, `ft.use_state`, `ft.use_memo`, `ft.use_dialog`) y se monta con `page.render(App, repo)`.

## Ejecutar

Desde la carpeta que contiene `finanzas/`:

```bash
pip install -r finanzas/requirements.txt
python3 -m finanzas.main
```

## Recorrido de demostración

1. Introduce una fecha AAAA-MM-DD, un concepto, una categoría, un tipo y un importe positivo.
2. Registra un ingreso de 1000.00 en Trabajo y un gasto de 125.50 en Comida.
3. Consulta el resumen: ingresos $1,000.00, gastos $125.50 y saldo $874.50.
4. Filtra por tipo `Ingreso`, categoría y mes para comprobar que tarjetas y tabla comparten los mismos registros.
5. Filtra una combinación sin movimientos: saldo $0.00, cero movimientos y mensaje de estado vacío.
6. Introduce `2026-13` como filtro de mes: no se aplica y se conservan los resultados anteriores con su etiqueta de alcance.
7. Prueba `1.005`, `NaN`, cero, negativos y una fecha imposible: no se guarda el registro.
8. Cierra y vuelve a abrir para comprobar persistencia. Prueba cancelar una eliminación antes de confirmarla.

## Estructura

- `dominio.py`: reglas puras (sin Flet ni SQL): conversión de importes con `Decimal`, validaciones, `Filtros`, `Movimiento` y `Resumen`.
- `repositorio.py`: SQLite, perfiles, migración desde la tabla antigua `gastos` y `ruta_por_defecto()`. Los métodos reciben el `perfil_id`; el repositorio no guarda selección.
- `componentes.py`: componentes de presentación (formulario, filtros, tarjetas, barras, tabla, diálogo de borrado).
- `app.py`: componente raíz `App`, con el estado de la pantalla.
- `main.py`: configuración de la página y arranque.
- `tests/`: dominio, repositorio y renderizado de la interfaz sin ventana.

## Reglas

Se aceptan punto o coma decimal, máximo dos decimales y ningún separador de miles. El máximo por movimiento es 9,999,999.99 MXN. No se redondea silenciosamente una entrada con más decimales. Las barras indican la proporción del **total filtrado** y mantienen separadas las categorías de ingresos y gastos; no son presupuestos ni metas. Las entradas se suman al saldo y las salidas se restan.

Las bases existentes con tabla `gastos` se migran como movimientos de tipo `Gasto`; la tabla antigua se conserva como respaldo y sus movimientos se asignan al perfil inicial (Ulises). No se agregan movimientos de ejemplo.

## Datos

La base se crea en `~/.fletBD/finanzas.sqlite3`; usa `FLET_DATA_DIR` para elegir otro directorio. Permite perfiles locales sin contraseña con movimientos separados. Sin conexión bancaria, autenticación, conversión de monedas ni sincronización; no está pensada como servicio multiusuario.

## Pruebas

```bash
python3 -m unittest discover -s finanzas/tests -t .
```

Referencias: [DataTable](https://flet.dev/docs/controls/datatable/) y [ProgressBar](https://flet.dev/docs/controls/progressbar/).
