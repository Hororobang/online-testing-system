from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
db = SQLAlchemy()

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="user"
    )


class Test(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text
    )


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)

    score = db.Column(db.Integer)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
class Question(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    test_id = db.Column(
        db.Integer,
        db.ForeignKey("test.id")
    )

    question = db.Column(
        db.Text,
        nullable=False
    )

    option1 = db.Column(db.String(255))
    option2 = db.Column(db.String(255))
    option3 = db.Column(db.String(255))
    option4 = db.Column(db.String(255))

    correct_answer = db.Column(
        db.String(255)
    )