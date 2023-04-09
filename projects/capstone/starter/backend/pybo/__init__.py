from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown
from sqlalchemy import MetaData

import config

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()


def create_app(**override):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config.update(override)
    app.url_map.strict_slashes = False

    # middleware

    # CORS
    CORS(app)

    # orm
    db.init_app(app)
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    # markdown
    Markdown(app, extensions=["nl2br", "fenced_code"])

    # views
    from . import views

    app.register_blueprint(views.bp)

    return app
