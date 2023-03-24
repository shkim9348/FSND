from flask import Blueprint, abort, json, jsonify, render_template, request, request_started, url_for, g, flash, session
from ..database.models import db, Question, Answer, User
from datetime import datetime
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
from ..auth.auth import requires_auth

bp = Blueprint("main", __name__, url_prefix="/")

# Home
@bp.route("/")
def index():
    return jsonify({"success": True}), 200

# QuestionList
@bp.route("/question/list", methods=["GET"])
def _list():
    page = request.args.get("page", type=int, default=1)
    kw = request.args.get("kw", type=str, default="")
    question_list = Question.query.order_by(Question.pinned.desc(), Question.create_date.desc())
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
    question_list = question_list.paginate(page=page, per_page=10)

    questions = [question.as_dict() for question in question_list.items]

    data={
        "questions": questions,
        "paginate": {
            "has_prev": question_list.has_prev,
            "has_next": question_list.has_next,
        }
    }
    return jsonify(data), 200

# QuestionDetail
@bp.route("/question/detail/<int:question_id>/")
def detail(question_id):
    question = Question.query.get_or_404(question_id)

    # 답변도 조회될 수 있도록 테이블 수정이 필요해 보임.

    return jsonify(question.as_dict()), 200

# CreateQuestion
@bp.route("/question/create/", methods=["POST"])
def create_question():
    data = request.get_json()
    question_data = {
        "subject": data.get("subject"),
        "content": data.get("content"),
        "user_id":data.get("user_id"),
        "pinned": data.get("pinned"),
    }

    if not all(question_data):
        abort(400)

    # crate question
    question = Question(**question_data)
    question.insert()

    return jsonify({"message": "Question successfully created."}), 200

# QuestionModify
@bp.route("/question/modify/<int:question_id>", methods=["POST"])
def modify_question(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        abort(403)

    data = request.get_json()
    question.subject = data.get("subject")
    question.content = data.get("content")
    question.pinned = data.get("pinned")
    question.modify_date = datetime.now()

    question.update()

    return jsonify({"message": "Question successfully modified."}), 200

# DeleteQuestion
@bp.route("/question/delete/<int:question_id>")
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        abort(403)

    question.delete()

    return jsonify({"message": "Question successfully deleted."}), 200

# QuestionVote
@bp.route("/question/vote/<int:question_id>/", methods=["POST"])
def vote_question(question_id):
    question = Question.query.get_or_404(question_id)
    
    if g.user == _question.user:
        return jsonify({"error": "본인이 작성한 글은 추천할 수 없습니다."}), 400

    if g.user in question.voter:
        question.voter.remove(g.user)
        message = "추천이 취소되었습니다."
    else:
        question.voter.append(g.user)
        message = "추천이 완료되었습니다."

    question.update()

    return jsonify({"message": "Successfully voted."}), 200

# CreateAnswer
@bp.route("/answer/create/<int:question_id>", methods=("POST",))
def create_answer(question_id):
    question = Question.query.get_or_404(question_id)
    data = request.get_json()
    content = data.get("content")
    user_id = data.get("user_id")

    answer = Answer(question = question, content = content, user_id = user_id)
    answer.insert()

    return jsonify({"message": "Answer successfully created."}), 200

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
    new_user = User(
        username=username,
        password=generate_password_hash(password),
        email=email
    )
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

    return jsonify({"message":"로그아웃 되었습니다."}), 200
