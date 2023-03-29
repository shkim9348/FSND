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


class Question(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", backref=db.backref("question_set"))
    modify_date = db.Column(db.DateTime(), nullable=True)

    voter = db.relationship(
        "User",
        secondary=question_voter,
        backref=db.backref("question_voter_set"),
    )

    def __init__(self, subject, content, create_date, user):
        self.subject = subject
        self.content = content
        self.create_date = create_date
        self.user = user

    def as_dict(self):
        return {
            "id": self.id,
            "subject": self.subject,
            "content": self.content,
            "answer_set": [a.as_dict() for a in self.answer_set],
            "user": self.user.as_dict(),
            "create_date": self.create_date,
            "modify_date": self.modify_date,
        }


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

    def __init__(self, question, content, user_id):
        self.question = question
        self.content = content
        self.user_id = user_id

    def as_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "user": self.user.as_dict(),
            "create_date": self.create_date,
            "modify_date": self.modify_date,
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def as_dict(self):
        return {
            "username": self.username,
        }
