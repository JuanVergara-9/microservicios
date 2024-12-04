class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:12345678@localhost:5432/inventario_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = 'redis'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = 'redis://redis:6379/0'
