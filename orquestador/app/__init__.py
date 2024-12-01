from flask import Flask
from app.routes import api_bp
from app.extension import db, cache

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Inicializar extensiones
    db.init_app(app)
    cache.init_app(app)

    # Registrar blueprint de rutas
    app.register_blueprint(api_bp)

    return app