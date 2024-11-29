from flask import Flask
from flask_caching import Cache
from compras_app.routes import compras_bp
from compras_app.models import db

cache = Cache()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Inicializar SQLAlchemy
    db.init_app(app)
    
    # Inicializar caché
    cache.init_app(app)

    # Registrar blueprint de rutas
    app.register_blueprint(compras_bp)

    return app