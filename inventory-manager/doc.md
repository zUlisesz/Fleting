# API de `ExcelAPI`

Permite consultar y modificar las filas de `Inventario.xlsx` desde Python. Usa los encabezados de la hoja como nombres de campo. Si no se indica otra configuración, abre el archivo junto a `scrip.py`, selecciona la hoja activa y toma la primera fila como encabezados.

**Fecha:** 2026-09-29  
**Descripción:** Referencia breve de la API y la interfaz Flet para leer y modificar inventarios XLSX.  
**Archivos modificados:** `scrip.py`, `app.py`, `doc.md`, `requirements.txt`.

## Métodos

| Método | Entradas | Salida |
| --- | --- | --- |
| `ExcelAPI(filepath, sheet_name=None, header_row=1, key_column="Código", expected_headers=None)` | Archivo XLSX y, opcionalmente, hoja, fila de encabezados, columna clave y lista de columnas esperadas. | Instancia lista para trabajar; rechaza una estructura distinta si se indican columnas esperadas. |
| `get_all(filters=None, limit=None, offset=0)` | Filtros exactos por encabezado y paginación opcional. | Lista de filas como diccionarios. |
| `find(criteria)` | Diccionario de columnas y valores exactos. | Lista de filas coincidentes. |
| `get_one(criteria)` | Criterios exactos que deberían identificar una fila. | Diccionario, o `None`; genera error si hay varias coincidencias. |
| `get_by_code(code)` | Valor de `Código`. | Producto encontrado, o `None`. |
| `search(query, columns=None, case_sensitive=False)` | Texto, columnas opcionales y sensibilidad a mayúsculas. | Filas que contienen el texto. Por defecto busca en todas las columnas sin distinguir mayúsculas. |
| `add(record)` | Diccionario con los campos a agregar. | Fila agregada como diccionario. Rechaza códigos duplicados cuando existe `Código`. |
| `update(criteria, changes)` | Criterios exactos y diccionario de cambios. | Cantidad de filas actualizadas. |
| `update_by_code(code, changes)` | Código del producto y campos por cambiar. | Cantidad de filas actualizadas. |
| `delete(criteria)` | Criterios exactos. | Cantidad de filas eliminadas. |
| `delete_by_code(code)` | Código del producto. | Cantidad de filas eliminadas. |
| `save(filepath=None)` | Ruta opcional de destino. | Ruta donde se guardó el XLSX. El archivo se reemplaza tras completar la escritura; una ruta nueva pasa a ser la ruta activa. |
| `close()` | Sin entradas. | Cierra el libro. También se cierra automáticamente al salir de `with`. |

Los nombres de campo deben coincidir con los encabezados del XLSX, por ejemplo `"Producto"`, `"Departamento"` o `"Existencia"`. Los cambios se mantienen en memoria hasta llamar a `save()`.

## Interfaz Flet

Instala las dependencias con `python3 -m pip install -r requirements.txt` y ejecuta `python3 app.py`. También puedes abrirla en el navegador con `flet run -w app.py`. El campo **Archivo XLSX** acepta una ruta escrita; **Examinar** permite elegir otro inventario en la aplicación de escritorio. **Cargar** valida que las diez columnas coincidan con `Inventario.xlsx`. El archivo activo se muestra bajo el selector.

La pantalla permite buscar y filtrar productos, recorrer resultados de 25 en 25, agregar, editar y eliminar con confirmación. Cada cambio se guarda de inmediato en el archivo activo. Para trabajar con el inventario de otro día, selecciona su ruta y pulsa **Cargar**.

## Ejemplo

```python
from scrip import ExcelAPI

with ExcelAPI("Inventario.xlsx") as inventario:
    productos = inventario.search("broca", columns=["Producto"])
    producto = inventario.get_by_code("100098")
    inventario.update_by_code("100098", {"Existencia": 5})
    inventario.save("Inventario_actualizado.xlsx")
```
