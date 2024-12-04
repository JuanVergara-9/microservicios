from flask import Flask
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
cache = Cache()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Inicializar SQLAlchemy
    db.init_app(app)
    
    # Inicializar caché
    cache.init_app(app)
    
    # Inicializar migraciones
    migrate.init_app(app, db)

    # Registrar blueprints
    from app.routes import inventario_bp
    app.register_blueprint(inventario_bp)

    return app