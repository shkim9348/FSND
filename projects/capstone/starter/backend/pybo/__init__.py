import config
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown
from sqlalchemy import MetaData
from pytz import timezone


def wants_json_response(request):
    mimetypes = request.accept_mimetypes
    return mimetypes["application/json"] >= mimetypes["text/html"]


naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # timezone
    # app.config["TIMEZONE"] = pytz.timezone("Asia/Seoul")

    # CORS
    CORS(app, supports_credentials=True)

    # orm
    db.init_app(app)
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    # models
    from . import models

    # views
    from .views import answer_views, auth_views, main_views, question_views

    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)

    @app.after_request
    def creds(res):
        # cors
        res.headers["Access-Control-Allow-Credentials"] = "true"
        res.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
        res.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        res.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        return res

    # markdown
    Markdown(app, extensions=["nl2br", "fenced_code"])

    # 필터
    from .filter import format_datetime

    app.jinja_env.filters["datetime"] = format_datetime

    # error

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify(
                {
                    "errors": {
                        "422": ["unprocessable"],
                    }
                }
            ),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify(
                {
                    "errors": {
                        "400": ["bad request"],
                    }
                }
            ),
            400,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify(
                {
                    "errors": {
                        "404": ["not found"],
                    }
                }
            ),
            404,
        )

    # fix circular import
    from pybo.auth import AuthError

    @app.errorhandler(AuthError)
    def auth_error(error):
        return (
            jsonify(
                {
                    "errors": {
                        "authentication error": [error.error["description"]],
                    }
                }
            ),
            error.status_code,
        )

    return app
