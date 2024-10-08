class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///compras.db'  # Si decides usar SQLAlchemy para persistir datos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
