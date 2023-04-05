from datetime import datetime

from flask import Blueprint, flash, g, render_template, request, url_for, jsonify
from pybo import db, wants_json_response
from pybo.auth import requires_auth
from pybo.forms import AnswerForm
from pybo.models import Answer, Question
from pybo.views.auth_views import login_required
from werkzeug.utils import redirect

bp = Blueprint("answer", __name__, url_prefix="/answer")


# Create Answer
@bp.route("/create/<int:question_id>", methods=("GET","POST"))
@requires_auth(permission="post:answer")
@login_required
def create(question_id):
    form = AnswerForm()
    question = db.get_or_404(Question, question_id)
    if form.validate_on_submit():
        content = request.form["content"]
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)
        question.answer_set.append(answer)
        db.session.commit()

        if wants_json_response(request):
            return jsonify(answer.as_dict()), 200

        return redirect(
            "{}#answer_{}".format(
                url_for("question.detail", question_id=question_id),
                answer.id,
            )
        )

    if wants_json_response(request):
        return jsonify({"errors": form.errors}), 400

    return render_template("question/question_detail.html", question=question, form=form)


# Modify Answer
@bp.route("/modify/<int:answer_id>", methods=("GET", "POST", "PUT"))
@requires_auth(permission="put:answer")
@login_required
def modify(answer_id):
    answer = db.get_or_404(Answer, answer_id)
    if g.user != answer.user:
        if wants_json_response(request):
            # form.errors format
            return jsonify({"errors": {"permission denied": ["수정권한이 없습니다."]}}), 403

        flash("수정권한이 없습니다")
        return redirect(url_for("question.detail", question_id=answer.question.id))

    if request.method == "POST" or request.method == "PUT":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()

            if wants_json_response(request):
                return jsonify(answer.as_dict()), 200

            return redirect(
                "{}#answer_{}".format(
                    url_for("question.detail", question_id=answer.question.id),
                    answer.id,
                )
            )

        if wants_json_response(request):
            return jsonify({"errors": form.errors}), 400

    else:
        form = AnswerForm(obj=answer)

    if wants_json_response(request):
        return jsonify(answer.as_dict()), 200

    return render_template("answer/answer_form.html", form=form)


# Delete Answer
@bp.route("/delete/<int:answer_id>", methods=("GET", "DELETE"))
@requires_auth(permission="delete:answer")
@login_required
def delete(answer_id):
    answer = db.get_or_404(Answer, answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        if wants_json_response(request):
            # form.errors format
            return jsonify({"errors": {"permission denied": ["삭제권한이 없습니다."]}}), 403

        flash("삭제권한이 없습니다")
    else:
        db.session.delete(answer)
        db.session.commit()

    if wants_json_response(request):
        return jsonify({}), 200

    return redirect(url_for("question.detail", question_id=question_id))


# Vote Answer
@bp.route("/vote/<int:answer_id>", methods=("GET", "POST"))
@requires_auth(permission="vote:answer")
@login_required
def vote(answer_id):
    _answer = db.get_or_404(Answer, answer_id)
    if g.user == _answer.user:
        if wants_json_response(request):
            return jsonify({"errors": {"permission denied": ["본인이 작성한 글은 추천할 수 없습니다"]}}), 403

        flash("본인이 작성한 글은 추천할수 없습니다")
    else:
        _answer.voter.append(g.user)
        db.session.commit()

    if wants_json_response(request):
        return jsonify([voter.as_dict() for voter in _answer.voter]), 200

    return redirect(
        "{}#answer_{}".format(
            url_for("question.detail", question_id=_answer.question.id),
            _answer.id,
        )
    )
