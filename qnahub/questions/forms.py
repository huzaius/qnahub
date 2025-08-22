from wtforms import TextAreaField, StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired




class AskQuestionForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    body = TextAreaField("Content", validators=[DataRequired()])
    tags = StringField("Tags")
    submit = SubmitField("Post Your Question")

