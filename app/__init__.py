from flask import Flask
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuración de seguridad
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

# Credenciales gestionadas en base de datos (tabla usuarios_admin)
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin1")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "cocorote2026")

from functools import wraps
from flask import session, redirect, url_for
from .database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Decorador para proteger rutas
def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped_view

# Inicialización de esquema y usuario administrador por defecto

def ensure_schema():
    """Crea tablas mínimas necesarias de forma idempotente."""
    conn = get_db_connection()
    # usuarios
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            saldo_favor INTEGER DEFAULT 0
        )
        """
    )
    # pagos
    conn.execute(
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
    # usuarios_admin
    conn.execute(
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


def ensure_admin_table_and_seed():
    conn = get_db_connection()
    # Asegurar que la tabla exista antes de insertar
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios_admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    # Crear admin por defecto si no existe
    row = conn.execute("SELECT id FROM usuarios_admin WHERE username = ?", (ADMIN_USERNAME,)).fetchone()
    if not row:
        pw_hash = generate_password_hash(ADMIN_PASSWORD)
        conn.execute(
            "INSERT INTO usuarios_admin (username, password_hash) VALUES (?, ?)",
            (ADMIN_USERNAME, pw_hash)
        )
        conn.commit()
    conn.close()


def generar_facturas_mensuales():
    """Genera facturas pendientes para todos los usuarios al inicio de cada mes."""
    mes_actual = datetime.now().strftime("%Y-%m")
    conn = get_db_connection()
    usuarios = conn.execute("SELECT id, saldo_favor FROM usuarios").fetchall()
    for usuario in usuarios:
        # Verificar si ya existe un pago para este mes
        existe = conn.execute("SELECT id FROM pagos WHERE usuario_id = ? AND mes = ?", (usuario['id'], mes_actual)).fetchone()
        if not existe:
            saldo = usuario['saldo_favor'] or 0
            valor_factura = max(0, 12000 - saldo)
            # Aplicar saldo_favor: reducir factura, y si saldo >=12000, no generar o generar 0
            nuevo_saldo = max(0, saldo - 12000)
            conn.execute("UPDATE usuarios SET saldo_favor = ? WHERE id = ?", (nuevo_saldo, usuario['id']))
            # valor=0 significa pendiente; se paga después
            conn.execute("INSERT INTO pagos (usuario_id, mes, valor, pagado, estado) VALUES (?, ?, 0, 0, 'pendiente')", (usuario['id'], mes_actual))
    conn.commit()
    conn.close()

# Importar rutas al final para evitar importaciones circulares
from . import routes