from flask import Flask
from app.routes import compras_bp
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Inicializar SQLAlchemy
    db.init_app(app)

    # Registrar blueprint de rutas
    app.register_blueprint(compras_bp)

    return app