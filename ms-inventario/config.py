class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///inventario.db'  # Opcional, si decides usar base de datos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
