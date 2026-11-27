"""Configuración de la conexión a MySQL a partir de variables de entorno (``.env``)."""

import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

ENV_FILE = Path(__file__).resolve().parents[1] / ".env"
CONNECTION_TIMEOUT = 5  # segundos; evita que la app se congele si el servidor no responde

load_dotenv(dotenv_path=ENV_FILE)


def get_connection():
    """Abre una conexión con los datos de ``RECETARIO_DB_*``."""
    return mysql.connector.connect(
        host=os.getenv("RECETARIO_DB_HOST", "localhost"),
        port=int(os.getenv("RECETARIO_DB_PORT", "3306")),
        user=os.getenv("RECETARIO_DB_USER", "root"),
        password=os.getenv("RECETARIO_DB_PASSWORD", ""),
        database=os.getenv("RECETARIO_DB_NAME", "coocking"),
        connection_timeout=CONNECTION_TIMEOUT,
    )
