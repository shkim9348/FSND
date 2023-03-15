from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

"""
setup_db(app)
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


class Question(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)


class Answer(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id", ondelete="CASCADE"))
    question = db.relationship("Question", backref=db.backref("answer_set"))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
