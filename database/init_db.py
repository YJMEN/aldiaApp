import os
import sqlite3
from werkzeug.security import generate_password_hash

# Asegurar que trabajamos sobre la misma ruta que usa la app
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'aldiaapp.db')

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Crear tablas de forma idempotente
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS pagos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        mes TEXT,
        valor INTEGER,
        pagado INTEGER,
        estado TEXT,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS usuarios_admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TEXT DEFAULT (datetime('now'))
    )
    """
)



conn.commit()
conn.close()

print(f"Base de datos inicializada en: {DB_PATH}")
