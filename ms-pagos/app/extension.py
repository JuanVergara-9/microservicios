from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

# Inicializar las extensiones
db = SQLAlchemy()
cache = Cache()