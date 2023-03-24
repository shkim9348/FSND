from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

db = SQLAlchemy()
migrate = Migrate()

"""
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app):
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        db.create_all()


class BaseModel(db.Model):
    __abstract__ = True

    def __init__(self):
        pass

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        raise NotImplementedError


question_voter = db.Table(
    "question_voter",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "question_id",
        db.Integer,
        db.ForeignKey("question.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

answer_voter = db.Table(
    "answer_voter",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "answer_id",
        db.Integer,
        db.ForeignKey("answer.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Question(BaseModel):
    __tablename__ = "question"

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True)
    pinned = db.Column(db.Boolean())

    voter = db.relationship(
        "User", secondary=question_voter, backref=db.backref("question_voter_set")
    )
    user = db.relationship("User", backref=db.backref("question_set"))

    # 답변도 조회할 수 있도록 수정해야할 듯 함.

    def __init__(self, subject, content, user_id, pinned):
        self.subject = subject
        self.content = content
        self.create_date = datetime.now()
        self.user_id = user_id
        self.pinned = pinned

    def as_dict(self):
        return {
            "id": self.id,
            "subject": self.subject,
            "content": self.content,
            "create_date": self.create_date,
            "user_id": self.user_id,
            "modify_date": self.modify_date,
            "pinned": self.pinned,
            "voter": self.voter,
            "user": self.user.as_dict() if self.user else None,
            "answer_set": [str(answer) for answer in self.answer_set],
        }


class Answer(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id", ondelete="CASCADE"))
    question = db.relationship("Question", backref=db.backref("answer_set"))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", backref=db.backref("answer_set"))
    modify_date = db.Column(db.DateTime(), nullable=True)

    voter = db.relationship("User", secondary=answer_voter, backref=db.backref("answer_voter_set"))

    def __str__(self):
        return f"Answer(id={self.id}, question_id={self.question_id}, content={self.content}, create_date={self.create_date}, user_id={self.user_id}, modify_date={self.modify_date})"

    def __init__(self, question, content, user_id):
        self.question = question
        self.content = content
        self.create_date = datetime.now()
        self.user_id = user_id

    def as_dict(self):
        return {
            "id": self.id,
            "question_id": self.question_id,
            "question": self.question,
            "content": self.content,
            # "create_date": self.create_date,
            "user_id": self.user_id,
            "user": self.user.as_dict() if self.user else None,
            # "modify_date": self.modify_date,
            "voter": self.voter,
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "username": self.username,
        }
