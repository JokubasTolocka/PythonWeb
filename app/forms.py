from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms import PasswordField
from wtforms import DateField
from wtforms import IntegerField
from wtforms.validators import DataRequired

class Login(FlaskForm):
    username = TextField('username', validators=[DataRequired("You need to enter the username to log in")], render_kw={"placeholder": "Enter username"})
    password = PasswordField('password', validators=[DataRequired("You need to enter the password to log in")], render_kw={"placeholder": "Enter password"})

class Register(FlaskForm):
    username = TextField('username', validators=[DataRequired("You need to enter the username to register")], render_kw={"placeholder": "Enter username"})
    password = PasswordField('password', validators=[DataRequired("You need to enter the password to register")], render_kw={"placeholder": "Enter password"})
    repeatPassword = PasswordField('repeatPassword', validators=[DataRequired("You need to repeat the password to register")], render_kw={"placeholder": "Repeat password"})

class Book(FlaskForm):
    title = TextField('title', validators=[DataRequired()], render_kw={"placeholder": "Book title"})
    author = TextField('author', validators=[DataRequired()], render_kw={"placeholder": "Book author"})
    dateReleased = DateField('dateReleased', format="%Y-%m-%d", validators=[DataRequired("Date doesn't match the format")], render_kw={"placeholder": "YYYY-MM-DD"})
    copies = IntegerField('copies')

class Request(FlaskForm):
    id = TextField('id')

class Return(FlaskForm):
    id = TextField('id')

class ChangePassword(FlaskForm):
    currentPassword = PasswordField('currentPassword', validators=[DataRequired("You need to enter the currentPassword to change password")], render_kw={"placeholder": "Enter current password"})
    password = PasswordField('password', validators=[DataRequired("You need to enter the password to change password")], render_kw={"placeholder": "Enter new password"})
    repeatPassword = PasswordField('repeatPassword', validators=[DataRequired("You need to repeat the password to change password")], render_kw={"placeholder": "Repeat new password"})
