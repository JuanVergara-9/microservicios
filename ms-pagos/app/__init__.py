from flask import Flask
from flask_caching import Cache
from app.routes import pagos_bp
from app.models import db

cache = Cache()

def create_app():
    app = Flask(__name__)

    # Configuración desde archivo config.py
    app.config.from_object('config.Config')
    
    # Inicializar SQLAlchemy
    db.init_app(app)

    # Inicializar caché
    cache.init_app(app)

    # Registrar blueprint de rutas
    app.register_blueprint(pagos_bp)

    return app