# app/__init__.py
from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # SOLO MAIN POR AHORA
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    from app.routes.ia_chat import IAChatRoute
    ia_chat = IAChatRoute()
    app.register_blueprint(ia_chat.bp)
    


    return app