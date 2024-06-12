from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=64)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=64)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])

class ProfileForm(FlaskForm):
    profile = TextAreaField("Profile", validators=[DataRequired()])
    team_id = StringField("Team", validators=[DataRequired()])
    tags = StringField("Tags", validators=[DataRequired()])