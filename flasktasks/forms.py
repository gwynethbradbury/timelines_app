from flask_wtf import Form
from wtforms import StringField, PasswordField, TextField
from wtforms.validators import DataRequired, Email


class UsernamePasswordForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
class EmailPasswordForm(Form):
    username = TextField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class EmailForm(Form):
    email = TextField('Email', validators=[DataRequired(), Email()])

class PasswordForm(Form):
    password = PasswordField('Password', validators=[DataRequired()])