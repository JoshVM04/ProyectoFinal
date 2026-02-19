from flask import Flask


def create_app():

    app = Flask(__name__)


    # IMPORTAR RUTA IA
    from app.routes.ia_chat import IAChatRoute


    # CREAR OBJETO
    ia_chat = IAChatRoute()


    # REGISTRAR RUTA
    app.register_blueprint(ia_chat.bp)


    return app
