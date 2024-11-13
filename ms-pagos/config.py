class Config:
    DEBUG = True
    SECRET_KEY = 'tu_clave_secreta'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345678@postgres:5001/mydb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

