from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # SOLO IMPORTAMOS MAIN POR AHORA
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    # COMENTA TODO LO DEMÁS MIENTRAS
    # from app.routes.auth import auth_bp
    # from app.routes.destinos import destinos_bp
    # from app.routes.experiencias import experiencias_bp
    # from app.routes.ia_chat import ia_chat_bp
    
    # app.register_blueprint(auth_bp, url_prefix='/auth')
    # app.register_blueprint(destinos_bp, url_prefix='/destinos')
    # app.register_blueprint(experiencias_bp, url_prefix='/experiencias')
    # app.register_blueprint(ia_chat_bp, url_prefix='/ia-chat')

    return app