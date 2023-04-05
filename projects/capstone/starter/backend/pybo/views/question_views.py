from datetime import datetime

from flask import Blueprint, flash, g, render_template, request, url_for, jsonify
from pybo import wants_json_response
from pybo.auth import requires_auth
from pybo.forms import AnswerForm, QuestionForm
from pybo.models import Question, Answer, User
from pybo.views.auth_views import login_required
from werkzeug.utils import redirect

bp = Blueprint("question", __name__, url_prefix="/question")

from pybo import db


# Question List
@bp.route("/list/")
def _list():
    # page = request.args.get("page", type=int, default=1)  # 페이지
    # stmt = db.select(Question).order_by(Question.create_date.desc())
    # question_list = db.paginate(stmt, page=page, per_page=20)
    # return render_template("question/question_list.html", question_list=question_list)

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

    if wants_json_response(request):
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

    return render_template(
        "question/question_list.html", question_list=question_list, page=page, kw=kw
    )


# Question Detail
@bp.route("/detail/<int:question_id>/", methods=["GET"])
def detail(question_id):
    question = db.get_or_404(Question, question_id)

    if wants_json_response(request):
        return jsonify(question.as_dict()), 200

    form = AnswerForm()
    return render_template("question/question_detail.html", question=question, form=form)


# Create Question
@bp.route("/create/", methods=("GET", "POST"))
@requires_auth(permission="post:question")
@login_required
def create():
    form = QuestionForm()
    if request.method == "POST" and form.validate_on_submit():
        question = Question(
            subject=form.subject.data,
            content=form.content.data,
            create_date=datetime.now(),
            user=g.user,
        )
        db.session.add(question)
        db.session.commit()

        if wants_json_response(request):
            return jsonify(question.as_dict()), 200

        return redirect(url_for("main.index"))

    if wants_json_response(request):
        return jsonify({"errors": form.errors}), 400

    return render_template("question/question_form.html", form=form)


# Modify Question
@bp.route("/modify/<int:question_id>", methods=["GET", "POST", "PUT"])
@requires_auth(permission="put:question")
@login_required
def modify(question_id):
    question = db.get_or_404(Question, question_id)
    if g.user != question.user:
        if wants_json_response(request):
            # form.errors format
            return jsonify({"errors": {"permission denied": ["수정권한이 없습니다."]}})

        flash("수정권한이 없습니다")
        return redirect(url_for("question.detail", question_id=question_id))
    if request.method == "POST" or request.method == "PUT":  # POST 요청
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()

            if wants_json_response(request):
                return jsonify(question.as_dict()), 200

            return redirect(url_for("question.detail", question_id=question_id))

        if wants_json_response(request):
            return jsonify({"errors": form.errors}), 400

    else:  # GET 요청
        form = QuestionForm(obj=question)

    if wants_json_response(request):
        return jsonify(question.as_dict()), 200

    return render_template("question/question_form.html", form=form)


# Delete Question
@bp.route("/delete/<int:question_id>", methods=["GET", "DELETE"])
@requires_auth(permission="delete:question")
@login_required
def delete(question_id):
    question = db.get_or_404(Question, question_id)
    if g.user != question.user:
        if wants_json_response(request):
            # form.errors format
            return jsonify({"errors": {"permission denied": ["삭제권한이 없습니다."]}})

        flash("삭제권한이 없습니다")
        return redirect(url_for("question.detail", question_id=question_id))
    db.session.delete(question)
    db.session.commit()

    if wants_json_response(request):
        return jsonify({}), 200

    return redirect(url_for("question._list"))


# Vote Question
@bp.route("/vote/<int:question_id>", methods=["GET", "POST"])
@requires_auth(permission="vote:question")
@login_required
def vote(question_id):
    _question = db.get_or_404(Question, question_id)
    if g.user == _question.user:
        if wants_json_response(request):
            # form.errors format
            return jsonify({"errors": {"permission denied": ["본인이 작성한 글은 추천할수 없습니다"]}})

        flash("본인이 작성한 글은 추천할수 없습니다")
    else:
        _question.voter.append(g.user)
        db.session.commit()

    if wants_json_response(request):
        return jsonify([voter.as_dict() for voter in _question.voter]), 200

    return redirect(url_for("question.detail", question_id=question_id))
