from flask import Flask

app = Flask(__name__)

# Configuraciones
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'

from app.routes import main

app.register_blueprint(main.bp)