import os
from flask import Flask, jsonify
from flask_cors import CORS
from .database.models import setup_db
from config import app_config
from .auth.auth import AuthError


def create_app():
    app = Flask(__name__)
    env = os.environ.get("FLASK_ENV")
    if env == "development":
        app.config.from_object(app_config["development"])
    elif env == "product":
        app.config.from_object(app_config["product"])
    else:
        app.config.from_object(app_config["testing"])

    CORS(app)
    setup_db(app)
    from .views import main_views

    app.register_blueprint(main_views.bp)

    """
    error handlers
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "Bad request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "Not found"}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 422,
                    "message": "Can not process the request",
                }
            ),
            422,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify({"success": False, "error": 500, "message": "Internal server error"}),
            500,
        )

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify({"success": False, "error": ex.status_code, "message": ex.error})
        response.status_code = ex.status_code
        return response

    return app
