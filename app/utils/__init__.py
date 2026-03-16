from flask import Flask
from app.routes.routes import auth

def create_app():
    app = Flask(__name__)

    app.secret_key = "nomada_secret"

    # registrar rutas de autenticación
    app.register_blueprint(auth, url_prefix="/auth")

    return app