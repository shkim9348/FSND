import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(32)


class DevelopmentConfig(Config):
    DEBUG = True
    database_name = "pybo.db"
    database_path = "sqlite:///{}".format(os.path.join(basedir, database_name))
    SQLALCHEMY_DATABASE_URI = database_path


class TestingConfig(Config):
    TESTING = True
    database_name = "pybo_test.db"
    database_path = "sqlite:///{}".format(os.path.join(basedir, database_name))
    SQLALCHEMY_DATABASE_URI = database_path


class Auth(object):
    AUTH0_DOMAIN = "dev-ka6gmvkeo7lnrjzv.us.auth0.com"
    ALGORITHMS = ["RS256"]
    API_AUDIENCE = "pybo"


app_config = {"development": DevelopmentConfig, "testing": TestingConfig, "auth": Auth}

FLASK_DEBUG = os.environ.get("FLASK_DEBUG", False)
