import os


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or 'hard to guess'

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
            'sqlite:///' + os.path.join(PROJECT_ROOT, 'app.db')

    DEBUG = True


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    Debug = True


class TestingConfig(Config):
    Testing = True

config_by_name = dict(
        dev=DevelopmentConfig,
        test=TestingConfig,
        prod=ProductionConfig
)

key = Config.SECRET_KEY
