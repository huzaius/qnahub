from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, TextAreaField, ValidationError
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo
from qnahub.models import User

# Registration Form
class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField("Email Address",
                        validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=35)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match"), Length(min=6, max=35)])
    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "That email is taken. Please choose a different one.")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is taken. Please choose a different one.")

#Login Form
class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            Length(min=6, max=35)
        ]
    )

    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

#Update User Profile Form
class UpdateProfileForm(FlaskForm):
    fullname = StringField("Full Name", validators=[Length(max=25)])
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField("Email Address",
                        validators=[DataRequired(), Email()])
    picture = FileField("Upload Picture", validators=[FileAllowed(["jpg", "png","jpeg"], "JPEG & PNG files only!")]) 
    
    submit = SubmitField("Update")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=current_user.email).first()
            if user:
                raise ValidationError(
                    "That email is taken. Please choose a different one.")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=current_user.username).first()
            if user:
                raise ValidationError(
                    "That username is taken. Please choose a different one.")

# Ask Quesion Form
class AskQuestionForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    body = TextAreaField("Content", validators=[DataRequired()])
    tags = StringField("Tags")
    submit = SubmitField("Post Your Question")

    # def separate_tags(self,tags):
    #     if self.tags.data:
    #         return [tag.strip() for tag in self.tags.data.split(",")]
        