import os
from flask import Flask
from flask import session, redirect, url_for, request
from .database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


def create_app(config_name=None):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_name or os.environ.get("FLASK_CONFIG", "config.DevelopmentConfig"))
    app.secret_key = app.config["SECRET_KEY"]

    from .routes import bp
    app.register_blueprint(bp)

    return app


# Decorador para proteger rutas
from functools import wraps

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("main.login", next=request.path))
        return view(*args, **kwargs)
    return wrapped_view


app = create_app()

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
    admin_username = app.config.get("ADMIN_USERNAME")
    admin_password = app.config.get("ADMIN_PASSWORD")
    # Crear admin solo si las credenciales están definidas mediante variables de entorno.
    if admin_username and admin_password:
        row = conn.execute("SELECT id FROM usuarios_admin WHERE username = ?", (admin_username,)).fetchone()
        if not row:
            pw_hash = generate_password_hash(admin_password)
            conn.execute(
                "INSERT INTO usuarios_admin (username, password_hash) VALUES (?, ?)",
                (admin_username, pw_hash)
            )
            conn.commit()
    conn.close()


def generar_facturas_mensuales():
    """Genera facturas pendientes para todos los usuarios al inicio de cada mes."""
    monthly_fee = app.config.get("MONTHLY_FEE", 12000)
    mes_actual = datetime.now().strftime("%Y-%m")
    conn = get_db_connection()
    usuarios = conn.execute("SELECT id, saldo_favor FROM usuarios").fetchall()
    for usuario in usuarios:
        existe = conn.execute("SELECT id FROM pagos WHERE usuario_id = ? AND mes = ?", (usuario['id'], mes_actual)).fetchone()
        if not existe:
            saldo = usuario['saldo_favor'] or 0
            nuevo_saldo = max(0, saldo - monthly_fee)
            conn.execute("UPDATE usuarios SET saldo_favor = ? WHERE id = ?", (nuevo_saldo, usuario['id']))
            conn.execute(
                "INSERT INTO pagos (usuario_id, mes, valor, pagado, estado) VALUES (?, ?, 0, 0, 'pendiente')",
                (usuario['id'], mes_actual)
            )
    conn.commit()
    conn.close()

