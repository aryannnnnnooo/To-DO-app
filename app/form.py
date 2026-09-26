from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="username cannot be empty!"), Length(min=4, max=25)])
    password = PasswordField("Password", validators=[DataRequired(message="password cannot be empty!"), Length(min=6)])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="username cannot be empty!"), Length(min=4, max=25)])
    password = PasswordField("Password", validators=[DataRequired(message="password cannot be empty!"), Length(min=6)])
    submit = SubmitField("Login")