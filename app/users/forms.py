from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.simple import PasswordField, BooleanField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField( 'Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(4, 10)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')