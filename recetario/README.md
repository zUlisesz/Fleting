# Recetario Personal 🍳

Aplicación de escritorio interactiva para gestionar y organizar recetas de cocina, ingredientes e instrucciones paso a paso, construida con **Python**, **Flet** y **MySQL**.

---

##  Características

- **Gestión de recetas**: Crear, consultar, editar y eliminar recetas.
- **Ingredientes e instrucciones**: Agregar ingredientes con cantidades/unidades y definir pasos ordenados de preparación.
- **Búsqueda en tiempo real**: Filtrar recetas por título al instante.
- **Interfaz moderna**: UI reactiva y limpia desarrollada con Flet (Flutter para Python).
- **Arquitectura en capas**: Separación clara en `domain`, `repositories`, `services` y capa de presentación.

---

##  Tecnologías

- **Lenguaje:** Python 3.x
- **Interfaz Gráfica:** [Flet](https://flet.dev/)
- **Base de Datos:** MySQL
- **Conector:** `mysql-connector-python`

---

##  Requisitos Previos

1. Servidor **MySQL** en ejecución en `localhost:3306`.
2. Python 3.9 o superior instalado.

---

##  Configuración e Instalación

### 1. Clonar o descargar el repositorio
```bash
git clone <url-del-repositorio>
cd recetario
```

### 2. Instalar dependencias
```bash
pip install flet mysql-connector-python
```

### 3. Configurar la base de datos
Crea la base de datos y ejecuta el script [schema.sql](file:///Users/romero/escuela/pythonP/fleting/proyectos/recetario/schema.sql):

```sql
CREATE DATABASE coocking;
USE coocking;
-- Ejecutar el contenido de schema.sql
```

### 4. Configurar credenciales
Crea o edita el archivo `passkey.py` en la raíz del proyecto con tu contraseña de MySQL:

```python
PASS = "tu_contraseña_mysql"
```

---

## ▶ Ejecución

Para iniciar la aplicación, ejecuta:

```bash
python app.py
```

---

##  Estructura del Proyecto

```text
recetario/
├── app.py                 # Punto de entrada y UI (Flet)
├── database/              # Conexión y configuración de la base de datos
├── domain/                # Modelos de entidad (Recipe, Ingredient, etc.)
├── repositories/          # Acceso a datos y consultas SQL
├── services/              # Lógica de negocio (RecipeService)
├── schema.sql             # Esquema de tablas de la base de datos
└── passkey.py             # Clave de acceso / credenciales
```
