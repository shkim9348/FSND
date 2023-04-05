from flask import Blueprint, abort, json, jsonify, render_template, request, session, url_for
from pybo import wants_json_response
from ..database.models import db, Question, Answer, User
from ..forms import QuestionForm, AnswerForm, UserCreateForm
from datetime import datetime
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
from ..auth.auth import requires_auth

bp = Blueprint("main", __name__, url_prefix="/")


# Home
@bp.route("/")
def index():
    return jsonify({"success": True}), 200


# Question List
@bp.route("/question/list", methods=["GET"])
def _list():
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
@bp.route("/question/detail/<int:question_id>/")
def detail(question_id):
    question = db.get_or_404(Question, question_id)

    if wants_json_response(request):
        return jsonify(question.as_dict()), 200

    form = AnswerForm()
    return render_template("question/question_detail.html", question=question, form=form)


# Create Question
@bp.route("/question/create/", methods=["POST"])
def create_question():
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
@bp.route("/question/modify/<int:question_id>", methods=["GET", "POST", "PUT"])
def modify_question(question_id):
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
@bp.route("/question/delete/<int:question_id>", methods=["GET", "DELETE"])
def delete_question(question_id):
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
@bp.route("/question/vote/<int:question_id>/", methods=["GET", "POST"])
def vote_question(question_id):
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


# Create Answer
@bp.route("/answer/create/<int:question_id>", methods=("GET","POST"))
def create_answer(question_id):
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


# ModifyAnswer
@bp.route("/answer/modify/<int:answer_id>", methods=("GET", "POST", "PUT"))
def modify_answer(answer_id):
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
@bp.route("/answer/delete/<int:answer_id>", methods=("GET", "DELETE"))
def delete_answer(answer_id):
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
@bp.route("/answer/vote/<int:answer_id>/", methods=("GET", "POST"))
def vote_answer(answer_id):
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


# SignUp
@bp.route("/auth/signup/", methods=["POST"])
def signup():
    data = request.get_json()

    # 클라이언트에서 전송한 데이터에서 필요한 필드들을 추출합니다.
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    # 중복 체크를 수행합니다.
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"message": "이미 존재하는 사용자입니다."}), 409

    # 새로운 사용자를 추가합니다.
    new_user = User(username=username, password=generate_password_hash(password), email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "회원가입이 완료되었습니다."}), 201


# Login
@bp.route("/login/", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    # 사용자 검증
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "사용자를 찾을 수 없습니다."}), 404
    # 암호화 된 패스워드 검증 시
    # elif not check_password_hash(user.password, password):
    elif not user.password:
        return jsonify({"message": "잘못된 비밀번호입니다."}), 401
    else:
        session["logged_in"] = True
        return jsonify({"message": "로그인 성공!"}), 200


# Logout
@bp.route("/logout/")
def logout():
    # 아래 한줄을 빼도 return 값이 같음..
    session.pop("logged_in", None)

    return jsonify({"message": "로그아웃 되었습니다."}), 200

