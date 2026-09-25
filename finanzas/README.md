# Balance · Flujo de efectivo personal

Fecha de creación: 19 de septiembre de 2026.

Demostración completa de Flet para registrar ingresos y gastos en MXN, consultar el saldo del flujo de efectivo, filtrar por categoría, tipo y mes, comparar categorías mediante barras y eliminar registros con confirmación. Almacenamiento SQLite local; importes como centavos enteros.

## Ejecutar
```bash
python3 -m finanzas.app
```

## Recorrido de demostración

1. Introduce una fecha AAAA-MM-DD, un concepto, una categoría, un tipo y un importe positivo.
2. Registra un ingreso de 1000.00 en Trabajo y un gasto de 125.50 en Comida.
3. Consulta el resumen: ingresos $1,000.00, gastos $125.50 y saldo $874.50.
4. Filtra por tipo `Ingreso`, categoría y mes para comprobar que las tarjetas y la tabla comparten los mismos registros.
5. Filtra una combinación sin movimientos: saldo $0.00, cero movimientos y mensaje de estado vacío.
6. Introduce `2026-13` como filtro de mes: no se aplica, y se conservan los resultados anteriores con su etiqueta de alcance.
7. Prueba `1.005`, `NaN`, cero, negativos y una fecha imposible: no se guarda el registro.
8. Cierra y vuelve a abrir para comprobar persistencia. Prueba cancelar una eliminación antes de confirmarla.

## Arquitectura y reglas

- `modelo.py`: Movimiento, conversión con Decimal, resumen de flujo de efectivo, migración y repositorio.
- `app.py`: formulario, filtros explícitos, tarjetas, tabla desplazable y barras.

Se aceptan punto o coma decimal, máximo dos decimales y ningún separador de miles. El máximo por movimiento es 9,999,999.99 MXN. No se redondea silenciosamente una entrada con más decimales. Las barras indican proporción del **total filtrado**; no son presupuestos ni metas. Las entradas se suman al saldo y las salidas se restan. Las bases existentes con tabla `gastos` se migran como movimientos de tipo `Gasto`; la tabla antigua se conserva como respaldo. No se agregan movimientos de ejemplo automáticamente.

La base se crea en `~/.fletDB/finanzas.sqlite3`. Usa `FLET_DATA_DIR` para elegir otro directorio. App para un usuario local, sin conexión bancaria, autenticación, conversión de monedas o sincronización de sesiones. No está preparada como servicio público multiusuario.

## Extensión sugerida

Añade edición y exportación CSV, conservando importes exactos y verificando que filtros, tabla y totales usen los mismos registros. Sesiones relacionadas: días 8, 20, 21, 22, 26 y 29.

Referencias: [DataTable](https://flet.dev/docs/controls/datatable/) y [ProgressBar](https://flet.dev/docs/controls/progressbar/).
