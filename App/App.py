# Importar librerías necesarias
from flask import Flask, render_template, redirect, url_for, request, session
import mysql.connector           # Para conexión con MySQL
from dotenv import load_dotenv   # Para leer el archivo .env
import os
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import bcrypt                   # Para encriptar contraseñas
from datetime import datetime

# ----------------------------
# Cargar variables de entorno
# ----------------------------
load_dotenv()  # Lee las variables definidas en .env

# Crear la aplicación Flask
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # Clave secreta para sesiones

# ----------------------------
# Configuración de Flask-Login
# ----------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirige al login si no está autenticado

# ----------------------------
# Conexión a la base de datos MySQL
# ----------------------------
db = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DB")
)
cursor = db.cursor(dictionary=True)  # Diccionario para obtener columnas por nombre

# ----------------------------
# Modelo de usuario para Flask-Login
# ----------------------------
class Usuario(UserMixin):
    def __init__(self, id, nombre, email, rol):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.rol = rol

# ----------------------------
# Función para cargar usuario desde Flask-Login
# ----------------------------
@login_manager.user_loader
def load_user(user_id):
    cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (user_id,))
    user = cursor.fetchone()
    if user:
        return Usuario(user["id_usuario"], user["nombre"], user["email"], user["rol"])
    return None

# ----------------------------
# Ruta de login
# ----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"].encode("utf-8")

        cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password, user["password"].encode("utf-8")):
            login_user(Usuario(user["id_usuario"], user["nombre"], user["email"], user["rol"]))
            return redirect(url_for("index"))
        else:
            error = "Usuario o contraseña incorrectos"  # <-- Flag de error

    return render_template("login.html", error=error)
  
# ----------------------------
# Ruta para registrar nuevas transacciones
# ---------------------------- 
@app.route("/transaccion", methods=["GET", "POST"])
@login_required
def nueva_transaccion():
    # Obtener cuentas del usuario para el select
    cursor.execute("SELECT * FROM cuenta WHERE id_usuario = %s", (current_user.id,))
    cuentas = cursor.fetchall()

    # Obtener categorías
    cursor.execute("SELECT * FROM categoria")
    categorias = cursor.fetchall()

    if request.method == "POST":
        id_cuenta = request.form["id_cuenta"]
        tipo = request.form["tipo"]
        categoria = request.form["categoria"]
        id_categoria = request.form.get("id_categoria") or None
        monto = request.form["monto"]
        fecha = request.form["fecha"] or datetime.today().strftime('%Y-%m-%d')

        # Insertar en la tabla transaccion
        cursor.execute("""
            INSERT INTO transaccion (id_cuenta, tipo, categoria, monto, fecha, id_categoria, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """, (id_cuenta, tipo, categoria, monto, fecha, id_categoria))
        db.commit()

        # Actualizar saldo de la cuenta
        if tipo == "ingreso":
            cursor.execute("UPDATE cuenta SET saldo_actual = saldo_actual + %s WHERE id_cuenta = %s", (monto, id_cuenta))
        else:
            cursor.execute("UPDATE cuenta SET saldo_actual = saldo_actual - %s WHERE id_cuenta = %s", (monto, id_cuenta))
        db.commit()

        flash("Transacción registrada correctamente.", "success")
        return redirect(url_for("index"))

    return render_template("nueva_transaccion.html", cuentas=cuentas, categorias=categorias)

# ----------------------------
# Ruta de registro de usuarios
# ----------------------------
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = request.form["password"].encode("utf-8")
        rol = request.form["rol"]  # 'admin' o 'usuario'

        # Hashear la contraseña
        hashed_pass = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")

        # Insertar en la base de datos
        try:
            cursor.execute(
                "INSERT INTO usuarios (nombre, email, password, rol) VALUES (%s, %s, %s, %s)",
                (nombre, email, hashed_pass, rol)
            )
            db.commit()
            return redirect(url_for("login"))
        except mysql.connector.Error as e:
            error_msg = f"Error al crear el usuario: {str(e)}"
            return render_template("registro.html", error=error_msg)

    # Si GET, mostrar el formulario
    return render_template("registro.html")


# ----------------------------
# Ruta de logout
# ----------------------------
@app.route("/logout")
@login_required  # Solo usuarios autenticados pueden cerrar sesión
def logout():
    logout_user()
    return redirect(url_for("login"))

# ----------------------------
# Dashboard principal
# ----------------------------
@app.route("/")
@login_required  # Solo usuarios autenticados pueden acceder
def index():
    user_id = current_user.id  # Obtener ID del usuario logueado

    # Consultar saldo total de usuario en la base de datos
    cursor.execute("SELECT SUM(monto) as saldo_total FROM transaccion WHERE id_usuario = %s", (user_id,))
    saldo = cursor.fetchone()
    saldo_total = saldo["saldo_total"] if saldo["saldo_total"] else 0  # Si no hay saldo, poner 0

    # Pasar datos al template
    data = {
        'Titulo': 'Dashboard',
        'SaldoTotal': saldo_total
    }
    return render_template("index.html", data=data)

# ----------------------------
# Ejecutar la aplicación
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Ejecuta el servidor Flask
