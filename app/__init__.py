# app/__init__.py
# Flask application factory - initializes the app and registers all blueprints

from flask import Flask
from config import Config

def create_app():
    """Create and configure the Flask application"""
    
    # Initialize Flask app with configuration
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register main routes (home page, static pages)
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    # importar clase POO IA
    from app.routes.ia_chat import IAChatRoutes

    ia_routes = IAChatRoutes()

    app.register_blueprint(ia_routes.blueprint)

    return app