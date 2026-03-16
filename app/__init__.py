from flask import Flask
from config import Config
import os

def create_app():
    # Especificar explícitamente la carpeta static
    static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    app = Flask(__name__, 
                static_folder=static_folder,
                static_url_path='/static')
    
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

    # Experiencias
    from app.routes.experiencias import ExperienciasRoutes
    experiencias_routes = ExperienciasRoutes()
    app.register_blueprint(experiencias_routes.blueprint)

    return app