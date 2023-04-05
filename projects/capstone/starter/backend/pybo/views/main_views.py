from flask import Blueprint, request, url_for, abort
from flask_wtf.csrf import generate_csrf
from werkzeug.utils import redirect


bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("/")
def index():
    return redirect(url_for("question.list"))


@bp.route("/csrftoken", methods=["GET"])
def get_csrf_token():

    # session csrf token
    return generate_csrf()
