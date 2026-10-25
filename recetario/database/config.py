import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv


ENV_FILE = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=ENV_FILE)


def get_connection():
    """Open a database connection using the Recetario environment settings."""
    return mysql.connector.connect(
        host=os.getenv("RECETARIO_DB_HOST", "localhost"),
        port=int(os.getenv("RECETARIO_DB_PORT", "3306")),
        user=os.getenv("RECETARIO_DB_USER", "root"),
        password=os.getenv("RECETARIO_DB_PASSWORD", ""),
        database=os.getenv("RECETARIO_DB_NAME", "coocking"),
    )
