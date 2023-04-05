from datetime import datetime

from flask import Blueprint, flash, g, render_template, request, url_for, jsonify
from pybo.auth import requires_auth
from pybo.forms import AnswerForm, QuestionForm
from pybo.models import Question, Answer, User
from werkzeug.utils import redirect

bp = Blueprint("", __name__, url_prefix="/question")

from pybo import db


# Question List
@bp.route("/", methods=["GET"])
def questions():
    page = request.args.get("page", type=int, default=1)
    kw = request.args.get("kw", type=str, default="")
    question_list = db.select(Question).order_by(Question.create_date.desc())
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
    question_list = db.paginate(question_list, page=page, per_page=10, error_out=False)

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
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(
            subject=form.subject.data,
            content=form.content.data,
            create_date=datetime.now(),
            user=g.user,
        )
        db.session.add(question)
        db.session.commit()

        return jsonify(question.as_dict()), 200

    return jsonify({"errors": form.errors}), 400


# Modify Question
@bp.route("/<int:question_id>", methods=["PUT"])
@requires_auth(permission="put:question")
def question_modify(question_id):
    question = db.get_or_404(Question, question_id)
    if g.user != question.user:
        # form.errors format
        return jsonify({"errors": {"permission denied": ["수정권한이 없습니다."]}}), 403

    form = QuestionForm()
    if form.validate_on_submit():
        form.populate_obj(question)
        question.modify_date = datetime.now()  # 수정일시 저장
        db.session.commit()

        return jsonify(question.as_dict()), 200

    return jsonify({"errors": form.errors}), 400


# Delete Question
@bp.route("/<int:question_id>", methods=["DELETE"])
@requires_auth(permission="delete:question")
def question_delete(question_id):
    question = db.get_or_404(Question, question_id)
    if g.user != question.user:
        # form.errors format
        return jsonify({"errors": {"permission denied": ["삭제권한이 없습니다."]}}), 403

    db.session.delete(question)
    db.session.commit()

    return jsonify({}), 200


# Vote Question
@bp.route("/<int:question_id>/vote", methods=["POST"])
@requires_auth(permission="vote:question")
def question_vote(question_id):
    question = db.get_or_404(Question, question_id)
    if g.user == question.user:
        # form.errors format
        return jsonify({"errors": {"permission denied": ["본인이 작성한 글은 추천할수 없습니다"]}}), 403

    else:
        question.voter.append(g.user)
        db.session.commit()

    return jsonify([voter.as_dict() for voter in question.voter]), 200


# Answer Detail
@bp.route("/<int:question_id>/answer/<int:answer_id>", methods=["GET"])
def answer_read(question_id, answer_id):
    answer = db.get_or_404(Answer, answer_id)
    return jsonify(answer.as_dict()), 200


# Modify Answer
@bp.route("/<int:question_id>/answer/<int:answer_id>", methods=["PUT"])
@requires_auth(permission="put:answer")
def answer_modify(question_id, answer_id):
    answer = db.get_or_404(Answer, answer_id)
    if g.user != answer.user:
        # form.errors format
        return jsonify({"errors": {"permission denied": ["수정권한이 없습니다."]}}), 403

    form = AnswerForm()
    if form.validate_on_submit():
        form.populate_obj(answer)
        answer.modify_date = datetime.now()  # 수정일시 저장
        db.session.commit()

        return jsonify(answer.as_dict()), 200

    return jsonify({"errors": form.errors}), 400


# Create Answer
@bp.route("/<int:question_id>/answer", methods=["POST"])
@requires_auth(permission="post:answer")
def answer_create(question_id):
    form = AnswerForm()
    question = db.get_or_404(Question, question_id)
    if form.validate_on_submit():
        content = request.form["content"]
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)
        question.answer_set.append(answer)
        db.session.commit()

        return jsonify(answer.as_dict()), 200

    return jsonify({"errors": form.errors}), 400


# Delete Answer
@bp.route("/<int:question_id>/answer/<int:answer_id>", methods=["DELETE"])
@requires_auth(permission="delete:answer")
def answer_delete(question_id, answer_id):
    answer = db.get_or_404(Answer, answer_id)
    if g.user != answer.user:
        # form.errors format
        return jsonify({"errors": {"permission denied": ["삭제권한이 없습니다."]}}), 403

    else:
        db.session.delete(answer)
        db.session.commit()

    return jsonify({}), 200


# Vote Answer
@bp.route("/<int:question_id>/answer/<int:answer_id>/vote", methods=["POST"])
@requires_auth(permission="vote:answer")
def answer_vote(question_id, answer_id):
    answer = db.get_or_404(Answer, answer_id)
    if g.user == answer.user:
        return jsonify({"errors": {"permission denied": ["본인이 작성한 글은 추천할 수 없습니다"]}}), 403

    else:
        answer.voter.append(g.user)
        db.session.commit()

    return jsonify([voter.as_dict() for voter in answer.voter]), 200

