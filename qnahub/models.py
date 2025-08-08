from datetime import datetime, timezone
from qnahub import db  # Note: Consider moving db to its own file to avoid circular imports.
from sqlalchemy import func, select
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # It's recommended to store hashed passwords, which might need more length.
    password = db.Column(db.String(255), nullable=False)
    fullname = db.Column(db.String(100), nullable=True)
    picture = db.Column(db.String(120), nullable=False, default="default.jpg")

    questions = db.relationship("Question", backref="author", lazy=True)
    answers = db.relationship("Answer", backref="author", lazy=True)
    votes = db.relationship("Vote", backref="voter", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.picture}')"

# Association table for the many-to-many relationship between Question and Tag
question_tags = db.Table('question_tags',
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"Tag('{self.name}')"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    date_posted = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    views = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)

    answers = db.relationship(
        "Answer", backref="question", lazy=True, cascade="all, delete-orphan"
    )
    votes_on_question = db.relationship(
        "Vote", backref="question", lazy=True, cascade="all, delete-orphan"
    )
    tags = db.relationship(
        "Tag", secondary=question_tags, backref=db.backref("questions", lazy="dynamic")
    )

    @hybrid_property
    def score(self):
        if self.votes_on_question:
            return sum(v.vote_type for v in self.votes_on_question)
        return 0

    @score.expression
    def score(cls):
        return (
            select(func.sum(Vote.vote_type))
            .where(Vote.question_id == cls.id)
            .label("total_score")
        )

    def __repr__(self):
        return f"Question('{self.title}', '{self.body}', '{self.date_posted}')"


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    # The 'votes' column is denormalized. It's better to calculate the score
    # from the Vote model to ensure data integrity.
    # votes = db.Column(db.Integer, default=0)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    votes_on_answer = db.relationship(
        "Vote", backref="answer", lazy=True, cascade="all, delete-orphan"
    )

    @hybrid_property
    def score(self):
        if self.votes_on_answer:
            return sum(v.vote_type for v in self.votes_on_answer)
        return 0

    @score.expression
    def score(cls):
        return (
            select(func.sum(Vote.vote_type)).where(Vote.answer_id == cls.id).label("total_score")
    )

    def __repr__(self):
        return f"Answer('{self.body}', '{self.timestamp}')"


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=True)
    answer_id = db.Column(db.Integer, db.ForeignKey("answer.id"), nullable=True)
    # e.g., +1 for upvote, -1 for downvote
    vote_type = db.Column(db.SmallInteger, nullable=False)

    __table_args__ = (
        db.CheckConstraint(
            "(question_id IS NOT NULL AND answer_id IS NULL) OR (question_id IS NULL AND answer_id IS NOT NULL)",
            name="ck_vote_target",
        ),
        db.UniqueConstraint("user_id", "question_id", name="uq_user_question_vote"),
        db.UniqueConstraint("user_id", "answer_id", name="uq_user_answer_vote"),
    )
