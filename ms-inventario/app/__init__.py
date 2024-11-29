from flask import Flask
from flask_caching import Cache
from app.routes import inventario_bp

cache = Cache()

def create_app():
    app = Flask(__name__)

    # Configuración desde archivo config.py
    app.config.from_object('config.Config')

    # Inicializar caché
    cache.init_app(app)

    # Registrar blueprint de rutas
    app.register_blueprint(inventario_bp)

    return app