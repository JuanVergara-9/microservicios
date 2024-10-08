from flask import Flask
from app.routes import inventario_bp

def create_app():
    app = Flask(__name__)

    # Configuración desde archivo config.py
    app.config.from_object('config.Config')

    # Registrar blueprint de rutas
    app.register_blueprint(inventario_bp)

    return app
