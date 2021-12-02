import os


class BaseConfig():
    API_PREFIX = '/api'
    TESTING = False
    DEBUG = True


class DevConfig(BaseConfig):
    FLASK_ENV = 'development'
    DEBUG = True
    POSTGRES_DB = os.environ.get('POSTGRES_DB', 'postgres')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT', 5432)
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'db-postgres')
    POSTGRES_USER = os.environ.get('POSTGRES_USER', 'admin')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'admin')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
