# app/__init__.py
from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register main routes
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    # IA Chat
    from app.routes.ia_chat import IAChatRoutes
    ia_routes = IAChatRoutes()
    app.register_blueprint(ia_routes.blueprint)

    # Destinos
    from app.routes.destinos import DestinosRoutes
    destinos_routes = DestinosRoutes()
    app.register_blueprint(destinos_routes.blueprint)

    # Autenticación
    from app.routes.auth import AuthRoutes
    auth_routes = AuthRoutes()
    app.register_blueprint(auth_routes.blueprint)

    # ===== EXPERIENCIAS =====
    from app.routes.experiencias import ExperienciasRoutes
    experiencias_routes = ExperienciasRoutes()
    app.register_blueprint(experiencias_routes.blueprint)

    return app