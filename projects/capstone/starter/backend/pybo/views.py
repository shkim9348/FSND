from datetime import datetime

from flask import Blueprint, abort, g, jsonify, request, session

from pybo import db
from pybo.auth import AuthError, requires_auth
from pybo.models import Answer, Question, RequiredError, User

# Blueprint
bp = Blueprint("api", __name__, url_prefix="/question")


# Question List
@bp.route("/", methods=["GET"])
def questions():
    # query string
    page = request.args.get("page", type=int, default=1)
    kw = request.args.get("kw", type=str, default="")

    # question list
    question_list = db.select(Question).order_by(Question.create_date.desc())

    # serarch
    if kw:
        search = "%%{}%%".format(kw)
        sub_query = (
            db.session.query(Answer.question_id, Answer.content, User.username)
            .join(User, Answer.user_id == User.id)
            .subquery()
        )
        question_list = (
            question_list.join(User)
            .outerjoin(sub_query, sub_query.c.question_id == Question.id)
            .filter(
                Question.subject.ilike(search)
                | Question.content.ilike(search)  # 질문제목
                | User.username.ilike(search)  # 질문내용
                | sub_query.c.content.ilike(search)  # 질문작성자
                | sub_query.c.username.ilike(search)  # 답변내용  # 답변작성자
            )
            .distinct()
        )

    # pagination
    question_list = db.paginate(
        question_list,
        page=page,
        per_page=10,
        error_out=False,
    )

    # api data
    data = {
        # question list
        "questions": [q.as_dict() for q in question_list.items],
        # pagination
        "total": question_list.total,
        "page": question_list.page,
        "per_page": question_list.per_page,
        "has_prev": question_list.has_prev,
        "prev_num": question_list.prev_num,
        "page_nums": list(question_list.iter_pages()),
        "has_next": question_list.has_next,
        "next_num": question_list.next_num,
        # search
        "kw": kw,
    }
    return jsonify(data), 200


# Question Detail
@bp.route("/<int:question_id>/", methods=["GET"])
def question_read(question_id):
    question = db.get_or_404(Question, question_id)
    return jsonify(question.as_dict()), 200


# Create Question
@bp.route("/", methods=["POST"])
@requires_auth(permission="post:question")
def question_create():
    subject = request.json.get("subject")
    content = request.json.get("content")

    question = Question(
        subject=subject,
        content=content,
        create_date=datetime.now(),
        user=g.user,
    )
    db.session.add(question)
    db.session.commit()

    return jsonify(question.as_dict()), 200


# Modify Question
@bp.route("/<int:question_id>", methods=["PUT"])
@requires_auth(permission="put:question")
def question_modify(question_id):
    question = db.get_or_404(Question, question_id)
    if g.user != question.user:
        return (
            jsonify(
                {"errors": {"permission denied": ["Do not have permission to edit."]}},
            ),
            403,
        )

    subject = request.json.get("subject")
    content = request.json.get("content")

    question.subject = subject
    question.content = content
    question.modify_date = datetime.now()  # 수정일시 저장
    db.session.commit()

    return jsonify(question.as_dict()), 200


# Delete Question
@bp.route("/<int:question_id>", methods=["DELETE"])
@requires_auth(permission="delete:question")
def question_delete(question_id):
    question = db.get_or_404(Question, question_id)

    if g.user != question.user:
        return (
            jsonify(
                {"errors": {"permission denied": ["Do not have permission to delete."]}},
            ),
            403,
        )

    db.session.delete(question)
    db.session.commit()

    return jsonify({}), 200


# Vote Question
@bp.route("/<int:question_id>/vote", methods=["POST"])
@requires_auth(permission="vote:question")
def question_vote(question_id):
    question = db.get_or_404(Question, question_id)
    if g.user == question.user:
        return (
            jsonify(
                {"errors": {"permission denied": ["Cannot recomended your own"]}},
            ),
            403,
        )

    question.voter.append(g.user)
    db.session.commit()

    return jsonify([voter.as_dict() for voter in question.voter]), 200


# Answer Detail
@bp.route("/<int:question_id>/answer/<int:answer_id>", methods=["GET"])
def answer_read(question_id, answer_id):
    answer = Answer.query.filter_by(id=answer_id, question_id=question_id).first()
    if not answer:
        abort(404)

    return jsonify(answer.as_dict()), 200


# Modify Answer
@bp.route("/<int:question_id>/answer/<int:answer_id>", methods=["PUT"])
@requires_auth(permission="put:answer")
def answer_modify(question_id, answer_id):
    answer = Answer.query.filter_by(id=answer_id, question_id=question_id).first()
    if not answer:
        abort(404)

    if g.user != answer.user:
        return (
            jsonify(
                {"errors": {"permission denied": ["Do not have permission to edit."]}},
            ),
            403,
        )

    answer.content = request.json.get("content")
    answer.modify_date = datetime.now() 
    db.session.commit()

    return jsonify(answer.as_dict()), 200


# Create Answer
@bp.route("/<int:question_id>/answer", methods=["POST"])
@requires_auth(permission="post:answer")
def answer_create(question_id):
    question = db.get_or_404(Question, question_id)

    answer = Answer(
        content=request.json.get("content"),
        create_date=datetime.now(),
        user=g.user,
    )
    question.answer_set.append(answer)
    db.session.commit()

    return jsonify(answer.as_dict()), 200


# Delete Answer
@bp.route("/<int:question_id>/answer/<int:answer_id>", methods=["DELETE"])
@requires_auth(permission="delete:answer")
def answer_delete(question_id, answer_id):
    answer = Answer.query.filter_by(id=answer_id, question_id=question_id).first()
    if not answer:
        abort(404)

    if g.user != answer.user:
        return (
            jsonify(
                {"errors": {"permission denied": ["Do not have permission to delete."]}},
            ),
            403,
        )

    db.session.delete(answer)
    db.session.commit()

    return jsonify({}), 200


# Vote Answer
@bp.route("/<int:question_id>/answer/<int:answer_id>/vote", methods=["POST"])
@requires_auth(permission="vote:answer")
def answer_vote(question_id, answer_id):
    answer = db.get_or_404(Answer, answer_id)
    if answer.question_id != question_id:
        abort(404)

    if g.user == answer.user:
        return (
            jsonify(
                {"errors": {"permission denied": ["Cannot recomended your own"]},},
            ),
            403,
        )

    answer.voter.append(g.user)
    db.session.commit()

    return jsonify([voter.as_dict() for voter in answer.voter]), 200


# Error handler
@bp.app_errorhandler(400)
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


@bp.app_errorhandler(404)
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


@bp.app_errorhandler(422)
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


@bp.app_errorhandler(AuthError)
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


@bp.app_errorhandler(RequiredError)
def validation_error(error):
    return (
        jsonify(
            {
                "errors": {
                    "required error": [error.error],
                }
            }
        ),
        error.status_code,
    )


# App request
@bp.after_app_request
def creds(res):
    res.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    res.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    res.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
    return res


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None

    g.user = db.session.get(User, user_id)
