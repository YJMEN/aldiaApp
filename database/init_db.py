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

# Seed admin por defecto si no existe
row = cur.execute("SELECT id FROM usuarios_admin WHERE username = ?", ("admin1",)).fetchone()
if not row:
    pw_hash = generate_password_hash("cocorote2026")
    cur.execute(
        "INSERT INTO usuarios_admin (username, password_hash) VALUES (?, ?)",
        ("admin1", pw_hash)
    )

conn.commit()
conn.close()

print(f"Base de datos inicializada en: {DB_PATH}")