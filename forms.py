from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     validators.DataRequired()])
    submit = SubmitField('Sign Up')


class LoginForm(Form):
    email = StringField('Email', [validators.Length(min=6, max=35)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
