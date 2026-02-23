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

    # Register AI chat routes with /ia prefix
    # All chat URLs will start with /ia (e.g., /ia, /ia/chat)
    from app.routes.ia_chat import ia_chat_bp
    app.register_blueprint(ia_chat_bp, url_prefix='/ia')

    return app