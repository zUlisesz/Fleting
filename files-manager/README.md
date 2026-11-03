# Gestor de archivos

Aplicación local de Flet para explorar una carpeta, crear subcarpetas y eliminar elementos con confirmación.

## Ejecutar

```bash
cd files-manager
python3 app.py
```

## Alcance de seguridad

La carpeta inicial es el límite de navegación de la sesión. La aplicación permite entrar a subcarpetas y volver a sus niveles superiores dentro de ese límite, pero no salir de él. Al llegar a la carpeta inicial, el botón para subir informa que ya no hay un nivel disponible. Las eliminaciones son permanentes y se solicitan con confirmación.

## Estructura

- `app.py`: interfaz y acciones del usuario.
- `back.py`: navegación y operaciones de archivos acotadas a la carpeta inicial.
- `test_back.py`: pruebas de navegación segura.
