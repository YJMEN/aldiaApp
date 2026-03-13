from flask import Flask, render_template, request, redirect, url_for, session
from database.database import get_db_connection
import os
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuración de seguridad
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")
# Credenciales gestionadas en base de datos (tabla usuarios_admin)

# Decorador para proteger rutas
def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped_view

# Inicialización de tabla de administradores y usuario por defecto

def ensure_admin_table_and_seed():
    conn = get_db_connection()
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
    row = conn.execute("SELECT id FROM usuarios_admin WHERE username = ?", ("admin1",)).fetchone()
    if not row:
        pw_hash = generate_password_hash("cocorote2026")
        conn.execute(
            "INSERT INTO usuarios_admin (username, password_hash) VALUES (?, ?)",
            ("admin1", pw_hash)
        )
        conn.commit()
    conn.close()


# Rutas de autenticación
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        conn = get_db_connection()
        admin = conn.execute(
            "SELECT id, username, password_hash FROM usuarios_admin WHERE username = ?",
            (username,)
        ).fetchone()
        conn.close()
        if admin and check_password_hash(admin["password_hash"], password):
            session["user"] = admin["username"]
            session["user_id"] = admin["id"]
            next_url = request.args.get("next") or url_for("inicio")
            return redirect(next_url)
        else:
            error = "Credenciales inválidas."
    return render_template("login.html", error=error)

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))

#ruta principal
@app.route("/")
@login_required
def inicio():
    return render_template("index.html")

#ruta de usuarios
@app.route("/users", methods=["GET", "POST"])
@login_required
def users():
    error = None
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        if nombre:
            conn = get_db_connection()
            conn.execute("INSERT INTO usuarios (nombre) VALUES (?)", (nombre,))
            conn.commit()
            conn.close()
            return redirect(url_for("users"))
        else:
            error = "El nombre no puede estar vacío."
    conn = get_db_connection()
    # Agregación: total pagado, adeuda/saldo y estado en base a 12000
    query = """
    SELECT u.id, u.nombre,
           COALESCE(SUM(p.valor), 0) AS pagado,
           CASE
             WHEN COALESCE(SUM(p.valor),0) = 0 THEN 'pendiente'
             WHEN COALESCE(SUM(p.valor),0) < 12000 THEN 'parcial'
             ELSE 'aldia'
           END AS estado,
           CASE
             WHEN COALESCE(SUM(p.valor),0) < 12000 THEN 12000 - COALESCE(SUM(p.valor),0)
             ELSE 0
           END AS adeuda,
           CASE
             WHEN COALESCE(SUM(p.valor),0) > 12000 THEN COALESCE(SUM(p.valor),0) - 12000
             ELSE 0
           END AS saldo_favor
    FROM usuarios u
    LEFT JOIN pagos p ON p.usuario_id = u.id
    GROUP BY u.id, u.nombre
    ORDER BY u.id DESC
    """
    usuarios = conn.execute(query).fetchall()
    conn.close()
    return render_template("users.html", usuarios=usuarios, error=error)


@app.route("/users/<int:user_id>", methods=["GET"])
@login_required
def user_detail(user_id):
    conn = get_db_connection()
    usuario = conn.execute("SELECT id, nombre FROM usuarios WHERE id = ?", (user_id,)).fetchone()
    pagos = conn.execute(
        "SELECT id, mes, valor, pagado, estado FROM pagos WHERE usuario_id = ? ORDER BY id DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    if not usuario:
        return redirect(url_for("users"))
    return render_template("user_detail.html", usuario=usuario, pagos=pagos)


@app.route("/users/<int:user_id>/pagos", methods=["POST"]) 
@login_required
def create_pago(user_id):
    mes = request.form.get("mes", "").strip()
    valor_raw = request.form.get("valor", "").strip()
    estado = request.form.get("estado", "").strip() or None
    pagado = 1 if request.form.get("pagado") == "on" else 0

    try:
        valor = int(valor_raw)
    except ValueError:
        valor = None

    if not mes or valor is None:
        return redirect(url_for("user_detail", user_id=user_id))

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO pagos (usuario_id, mes, valor, pagado, estado) VALUES (?, ?, ?, ?, ?)",
        (user_id, mes, valor, pagado, estado)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("user_detail", user_id=user_id))



if __name__ == "__main__":
    with app.app_context():
        ensure_admin_table_and_seed()
    app.run(debug=True)