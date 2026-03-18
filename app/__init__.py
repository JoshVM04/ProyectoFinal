from flask import Flask
from config import Config
import os
import mysql.connector

def create_app():
    # Especificar explícitamente la carpeta static
    static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    app = Flask(__name__, 
                static_folder=static_folder,
                static_url_path='/static')
    
    app.config.from_object(Config)

    # ===== CREAR CONEXIÓN A LA BASE DE DATOS =====
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Admin",
        database="Nomada"
    )
    
    # Register main routes (no necesita BD)
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    # IA Chat (no necesita BD)
    from app.routes.ia_chat import IAChatRoutes
    ia_routes = IAChatRoutes()  # ← Sin conexión
    app.register_blueprint(ia_routes.blueprint)

    # Destinos (SÍ necesita BD)
    from app.routes.destinos import DestinosRoutes
    destinos_routes = DestinosRoutes(db_connection)  # ← Con conexión
    app.register_blueprint(destinos_routes.blueprint)

    # Autenticación (SÍ necesita BD)
    from app.routes.auth import AuthRoutes
    auth_routes = AuthRoutes(db_connection)  # ← Con conexión
    app.register_blueprint(auth_routes.blueprint)

    # Experiencias (SÍ necesita BD)
    from app.routes.experiencias import ExperienciasRoutes
    experiencias_routes = ExperienciasRoutes(db_connection)  # ← Con conexión
    app.register_blueprint(experiencias_routes.blueprint)

    return app