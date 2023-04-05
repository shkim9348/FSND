from pybo import db

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


class Question(db.Model):
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

    def as_dict(self):
        return {
            "id": self.id,
            "subject": self.subject,
            "answer_set": [a.as_dict() for a in self.answer_set],
            "user": self.user.as_dict(),
            "create_date": self.create_date,
            # detail
            "content": self.content,
            "modify_date": self.modify_date,
            "voter": [user.as_dict() for user in self.voter],
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


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id", ondelete="CASCADE"))
    question = db.relationship("Question", backref=db.backref("answer_set"))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", backref=db.backref("answer_set"))
    modify_date = db.Column(db.DateTime(), nullable=True)

    voter = db.relationship(
        "User",
        secondary=answer_voter,
        backref=db.backref("answer_voter_set"),
    )

    def as_dict(self):
        return {
            "id": self.id,
            # detail
            "content": self.content,
            "modify_date": self.modify_date,
            "user": self.user.as_dict(),
            "create_date": self.create_date,
            "voter": [user.as_dict() for user in self.voter],
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def as_dict(self):
        return {
            "username": self.username,
            # for auth0 frontend quth
            "email": self.email,
        }
