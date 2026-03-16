from flask import Blueprint, render_template, request, redirect, url_for, session
import mysql.connector
import bcrypt

auth = Blueprint('auth', __name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Nomada"
)

# LOGIN
@auth.route('/login', methods=['GET','POST'])
def login():

    if request.method == "POST":

        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM usuarios WHERE email=%s",(email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode(), user['password'].encode()):

            session['usuario_id'] = user['id']
            session['usuario_nombre'] = user['nombre']

            return redirect("/")

        return "Correo o contraseña incorrectos"

    return render_template("auth/login.html")


# REGISTER
@auth.route('/register', methods=['GET','POST'])
def register():

    if request.method == "POST":

        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        cursor = db.cursor()

        cursor.execute("""
        INSERT INTO usuarios (nombre,email,password)
        VALUES (%s,%s,%s)
        """,(nombre,email,hashed))

        db.commit()

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")