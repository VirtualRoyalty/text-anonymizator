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
    # CELERY_BROKER = 'pyamqp://rabbit_user:rabbit_password@broker-rabbitmq//'
    # CELERY_RESULT_BACKEND = 'rpc://rabbit_user:rabbit_password@broker-rabbitmq//'


# class ProductionConfig(BaseConfig):
#     FLASK_ENV = 'production'
#     SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_password@db-postgres:5432/flask-deploy'
#     CELERY_BROKER = 'pyamqp://rabbit_user:rabbit_password@broker-rabbitmq//'
#     CELERY_RESULT_BACKEND = 'rpc://rabbit_user:rabbit_password@broker-rabbitmq//'
#
#
# class TestConfig(BaseConfig):
#     FLASK_ENV = 'development'
#     TESTING = True
#     DEBUG = True
#     # make celery execute tasks synchronously in the same process
#     CELERY_ALWAYS_EAGER = True
