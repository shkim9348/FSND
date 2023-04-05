from flask import Blueprint, request, url_for, abort
from flask_wtf.csrf import generate_csrf
from werkzeug.utils import redirect

from pybo import wants_json_response

bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("/")
def index():
    return redirect(url_for("question._list"))


@bp.route("/csrftoken", methods=["GET"])
def get_csrf_token():
    if not wants_json_response(request):
        abort(404)

    # session csrf token
    return generate_csrf()
