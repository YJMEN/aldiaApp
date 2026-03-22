import os
import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime

def reset_db():
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'aldiaapp.db')

    # Eliminar la BD si existe
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    # Crear tablas
    conn.execute(
        """
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE pagos (
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
    conn.execute(
        """
        CREATE TABLE usuarios_admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )

    # Crear admin por defecto
    pw_hash = generate_password_hash("cocorote2026")
    conn.execute(
        "INSERT INTO usuarios_admin (username, password_hash) VALUES (?, ?)",
        ("admin1", pw_hash)
    )

    # Agregar algunos usuarios de prueba
    usuarios_prueba = ["Juan Pérez", "María García", "Carlos López", "Ana Rodríguez"]
    for nombre in usuarios_prueba:
        conn.execute("INSERT INTO usuarios (nombre) VALUES (?)", (nombre,))

    conn.commit()

    # Generar facturas para el mes actual
    mes_actual = datetime.now().strftime("%Y-%m")
    usuarios = conn.execute("SELECT id FROM usuarios").fetchall()
    for usuario in usuarios:
        conn.execute("INSERT INTO pagos (usuario_id, mes, valor, pagado, estado) VALUES (?, ?, 12000, 0, 'pendiente')", (usuario['id'], mes_actual))

    conn.commit()
    conn.close()

    print("Base de datos reseteada y facturas generadas para el mes actual.")

if __name__ == "__main__":
    reset_db()