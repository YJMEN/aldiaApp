from flask import render_template, request, redirect, url_for, session
from . import app
from .database import get_db_connection
from . import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

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
    conn = get_db_connection()
    current_month = datetime.now().strftime("%Y-%m")
    stats = conn.execute("""
    SELECT
      (SELECT COUNT(*) FROM usuarios) AS total_usuarios,
      SUM(CASE WHEN p.pagado=1 AND p.mes=? THEN 1 ELSE 0 END) AS total_pagaron,
      SUM(CASE WHEN p.pagado=0 AND p.mes=? THEN 1 ELSE 0 END) AS total_no_pagaron,
      COALESCE(SUM(CASE WHEN p.mes=? THEN p.valor ELSE 0 END), 0) AS total_recaudado
    FROM usuarios u
    LEFT JOIN pagos p ON p.usuario_id = u.id AND p.mes = ?
    """, (current_month, current_month, current_month, current_month)).fetchone()
    conn.close()
    return render_template("index.html", stats=stats, current_month=current_month)

#ruta de usuarios
@app.route("/users", methods=["GET", "POST"])
@login_required
def users():
    error = None
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip().title()
        if nombre:
            conn = get_db_connection()
            cur = conn.execute("INSERT INTO usuarios (nombre) VALUES (?)", (nombre,))
            new_user_id = cur.lastrowid
            mes_actual = datetime.now().strftime("%Y-%m")
            conn.execute(
                "INSERT INTO pagos (usuario_id, mes, valor, pagado, estado) VALUES (?, ?, 0, 0, 'pendiente')",
                (new_user_id, mes_actual)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("users"))
        else:
            error = "El nombre no puede estar vacío."
    conn = get_db_connection()
    # Agregación: total pagado, adeuda/saldo y estado en base a mensualidad de 12000
    query = """
    SELECT u.id, u.nombre, u.saldo_favor,
           COALESCE(SUM(p.valor), 0) AS pagado,
           CASE WHEN COALESCE(SUM(p.valor), 0) < 12000 THEN 12000 - COALESCE(SUM(p.valor), 0) ELSE 0 END AS adeuda,
           u.saldo_favor AS saldo_favor_real,
           CASE
             WHEN COALESCE(SUM(p.valor), 0) >= 12000 THEN 'aldia'
             WHEN COALESCE(SUM(p.valor), 0) > 0 THEN 'parcial'
             ELSE 'pendiente'
           END AS estado
    FROM usuarios u
    LEFT JOIN pagos p ON p.usuario_id = u.id
    GROUP BY u.id, u.nombre, u.saldo_favor
    ORDER BY u.id DESC
    """
    usuarios = conn.execute(query).fetchall()
    conn.close()
    return render_template("users.html", usuarios=usuarios, error=error)

@app.route("/reset_users", methods=["POST"])
@login_required
def reset_users():
    conn = get_db_connection()
    conn.execute("DELETE FROM pagos")
    conn.execute("DELETE FROM usuarios")
    conn.commit()
    conn.close()
    return redirect(url_for("users"))

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
    current_month = datetime.now().strftime("%Y-%m")
    return render_template("user_detail.html", usuario=usuario, pagos=pagos, current_month=current_month)

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

@app.route("/users/<int:user_id>/pagos/<int:pago_id>/pagar", methods=["POST"])
@login_required
def pagar_factura(user_id, pago_id):
    tipo = request.form.get("tipo_pago")
    porcentaje = request.form.get("valor_parcial", "0").strip()
    conn = get_db_connection()
    pago = conn.execute("SELECT * FROM pagos WHERE id = ? AND usuario_id = ?", (pago_id, user_id)).fetchone()
    if not pago:
        conn.close()
        return redirect(url_for("user_detail", user_id=user_id))

    pagado_acumulado = pago["valor"] or 0
    deuda_actual = 12000 - pagado_acumulado

    if tipo == "completo":
        valor_pagado = 12000 - pagado_acumulado  # Pagar lo restante para completar
        excedente = 0  # No excedente en completo
    else:
        try:
            pago_parcial = int(porcentaje)
        except ValueError:
            pago_parcial = 0
        if pago_parcial <= 0:
            conn.close()
            return redirect(url_for("user_detail", user_id=user_id))
        valor_pagado = min(pago_parcial, deuda_actual)
        excedente = max(0, pago_parcial - deuda_actual)  # Si paga más que la deuda actual

    if excedente > 0:
        # Agregar al saldo_favor del usuario
        usuario = conn.execute("SELECT saldo_favor FROM usuarios WHERE id = ?", (user_id,)).fetchone()
        nuevo_saldo = (usuario['saldo_favor'] or 0) + excedente
        conn.execute("UPDATE usuarios SET saldo_favor = ? WHERE id = ?", (nuevo_saldo, user_id))

    nuevo_pagado_acumulado = pagado_acumulado + valor_pagado
    pagado = 1 if nuevo_pagado_acumulado >= 12000 else 0
    estado = "aldia" if pagado == 1 else "parcial"

    conn.execute(
        "UPDATE pagos SET valor = ?, pagado = ?, estado = ? WHERE id = ?",
        (nuevo_pagado_acumulado, pagado, estado, pago_id)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("user_detail", user_id=user_id))

@app.route("/historial")
@login_required
def historial():
    conn = get_db_connection()
    current_month = datetime.now().strftime("%Y-%m")

    # Historial completo
    query = """
    SELECT p.id, p.mes, p.valor, p.pagado, p.estado, u.nombre as usuario_nombre
    FROM pagos p
    JOIN usuarios u ON p.usuario_id = u.id
    ORDER BY p.id DESC
    """
    pagos = conn.execute(query).fetchall()

    # Estadísticas del mes actual
    stat_query = """
    SELECT
      (SELECT COUNT(*) FROM usuarios) AS total_usuarios,
      SUM(CASE WHEN p.pagado=1 AND p.mes=? THEN 1 ELSE 0 END) AS total_pagaron,
      SUM(CASE WHEN p.pagado=0 AND p.mes=? THEN 1 ELSE 0 END) AS total_no_pagaron,
      COALESCE(SUM(CASE WHEN p.mes=? THEN p.valor ELSE 0 END), 0) AS total_recaudado
    FROM usuarios u
    LEFT JOIN pagos p ON p.usuario_id = u.id AND p.mes = ?
    """
    stats = conn.execute(stat_query, (current_month, current_month, current_month, current_month)).fetchone()

    conn.close()
    return render_template("history.html", pagos=pagos, current_month=current_month, stats=stats)