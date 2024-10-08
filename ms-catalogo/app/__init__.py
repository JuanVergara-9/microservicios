from flask import Flask
from app.routes import catalogo_bp

def create_app():
    app = Flask(__name__)

    # Configuración desde archivo
    app.config.from_object('config.Config')

    # Registrar blueprint de rutas
    app.register_blueprint(catalogo_bp)

    return app
