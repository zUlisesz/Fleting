# Recetario Personal 🍳

Aplicación de escritorio para gestionar recetas, ingredientes y pasos de preparación, construida con Python, Flet y MySQL.

## Características

- Crear, consultar, editar y eliminar recetas.
- Agregar ingredientes con cantidades y unidades, y definir pasos ordenados.
- Buscar recetas por título.
- Separar interfaz, dominio, acceso a datos y servicios.

## Requisitos

- Python 3.9 o superior.
- MySQL disponible en el host indicado en `.env`.

## Instalación y configuración

Desde la raíz del repositorio:

```bash
git clone https://github.com/zUlisesz/Fleting.git
cd Fleting/recetario
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Edita `.env` con los datos de conexión a MySQL. El archivo `.env` está ignorado por Git; no agregues contraseñas al repositorio.

Crea la base de datos y carga el esquema incluido en [`schema.sql`](schema.sql):

```sql
CREATE DATABASE coocking;
USE coocking;
```

Ejecuta después el contenido de `schema.sql` en esa base de datos.

## Ejecución

Desde la carpeta `recetario`, con el entorno virtual activado:

```bash
python app.py
```

## Pruebas

Desde la carpeta `recetario`, ejecuta las pruebas de servicio. Las operaciones de persistencia se simulan, así que no se necesita una base MySQL para esta suite:

```bash
python -m unittest discover -s tests -v
```

## Estructura

```text
recetario/
├── app.py                 # Punto de entrada y UI Flet
├── database/              # Configuración y conexión a MySQL
├── domain/                # Entidades Recipe, Ingredient e Instruction
├── repositories/          # Consultas y persistencia
├── services/              # Lógica de aplicación
├── requirements.txt       # Dependencias de este proyecto
├── .env.example           # Plantilla de configuración local
└── schema.sql             # Esquema de las tablas
```
