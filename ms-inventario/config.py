class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///inventario.db'  # Opcional, si decides usar base de datos
    SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345678@postgres:5002/mydb'
SQLALCHEMY_TRACK_MODIFICATIONS = False