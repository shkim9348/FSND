import os

BASE_DIR = os.path.dirname(__file__)


SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

# flask wtf
SECRET_KEY = "dev"

# api session sharing
# SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True

# auth0
AUTH0_DOMAIN = "dev-hwgb8d1f3r3ztqaq.us.auth0.com"
AUTH0_ALGORITHMS = ["RS256"]
API_AUDIENCE = "pybo"
