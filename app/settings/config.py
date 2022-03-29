import os
import logging
import datetime as dt

logger = logging.getLogger('backend')

POSTGRES_DB_PASSWORD = None
try:
    POSTGRES_DB_PASSWORD = os.environ["postgres_db_password"]
except: 
    logger.warning("No postgres password set in the os enviroment")

try:
    jwt_secret_key = os.environ["JWT_SECRET_KEY"]
except KeyError:
    logger.warn("No Secret key set in the os enviroment")
    jwt_secret_key = "a08e82d1d3e24f24a25bd3a2"

POSTGRES = {
    'user': 'postgres',
    'pw': POSTGRES_DB_PASSWORD,
    'db': 'logisticservice',
    'host': 'localhost',
    'port': '5432',
}


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    NAME = "development" #change it to APP_ENV
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = jwt_secret_key
    JWT_ACCESS_TOKEN_EXPIRES = dt.timedelta(days=30)
    JWT_USER_CLAIMS = "payload"
    JWT_IDENTITY_CLAIM = "sub"


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    POSTGRES["host"] = "localhost"
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


class DockerConfig(DevelopmentConfig):
    NAME = "docker"
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True
    NAME = "testing"
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True
    NAME = "staging"
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
    NAME = "production"
    POSTGRES["host"] = "polyglot.cxisjiaafl0q.eu-west-2.rds.amazonaws.com"
    POSTGRES["db"] = "backend_service"
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


app_config = {
    'development': DevelopmentConfig,
    'docker': DockerConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
