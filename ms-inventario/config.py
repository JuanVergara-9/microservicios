class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///inventario.db'  # Opcional, si decides usar base de datos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = 'redis'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = 'redis://redis:6379/0'

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345678@postgres:5002/mydb'
SQLALCHEMY_TRACK_MODIFICATIONS = False