from flask import Blueprint, jsonify
from ..auth.auth import requires_auth
bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("/api/board", methods=["GET"])
@requires_auth("get:board")
def get_board():
    board = [
        {"id": 1, "title": "Post 1", "content": "Post content 1"},
        {"id": 2, "title": "Post 2", "content": "Post content 2"},
    ]
    return jsonify(board)
