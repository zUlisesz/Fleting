# Balance · Panel de gastos personales

Fecha de creación: 19 de septiembre de 2026.

Demostración completa de Flet para registrar gastos en MXN, filtrar por categoría y mes, visualizar total y número de movimientos, comparar categorías mediante barras y eliminar registros con confirmación. Almacenamiento SQLite local; importes como centavos enteros.

## Ejecutar
```bash
python3 -m finanzas.app
```

## Recorrido de demostración

1. Introduce una fecha AAAA-MM-DD, un concepto, una categoría y un importe positivo.
2. Registra 10.10 y 20.20 en Estudio, con fechas de un mismo mes.
3. Filtra Estudio y ese mes: total $30.30 y dos movimientos.
4. Filtra una categoría sin gastos: total $0.00, cero movimientos y mensaje de estado vacío.
5. Introduce `2026-13` como filtro de mes: no se aplica, y se conservan los resultados anteriores con su etiqueta de alcance.
6. Prueba `1.005`, `NaN`, cero, negativos y una fecha imposible: no se guarda el registro.
7. Cierra y vuelve a abrir para comprobar persistencia. Prueba cancelar una eliminación antes de confirmarla.

## Arquitectura y reglas

- `modelo.py`: Gasto, conversión con Decimal, formateo, agrupación y repositorio.
- `app.py`: formulario, filtros explícitos, tarjetas, tabla desplazable y barras.

Se aceptan punto o coma decimal, máximo dos decimales y ningún separador de miles. El máximo por gasto es 9,999,999.99 MXN. No se redondea silenciosamente una entrada con más decimales. Las barras indican proporción del **total filtrado**; no son presupuestos ni metas. No se agregan gastos de ejemplo automáticamente.

La base se crea en `~/.fletDB/finanzas.sqlite3`. Usa `FLET_DATA_DIR` para elegir otro directorio. App para un usuario local, sin conexión bancaria, autenticación, conversión de monedas o sincronización de sesiones. No está preparada como servicio público multiusuario.

## Extensión sugerida

Añade edición y exportación CSV, conservando importes exactos y verificando que filtros, tabla y totales usen los mismos registros. Sesiones relacionadas: días 8, 20, 21, 22, 26 y 29.

Referencias: [DataTable](https://flet.dev/docs/controls/datatable/) y [ProgressBar](https://flet.dev/docs/controls/progressbar/).
