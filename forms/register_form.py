from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    email = StringField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_again = PasswordField("Повторите пароль", validators=[DataRequired()])
    about = StringField("Расскажи о себе", validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    sex = StringField('Пол', validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired()])
    submit = SubmitField("Зарегистрироваться")

class ChangeForm(FlaskForm):
    old_password = PasswordField("Старый пароль", validators=[DataRequired()])
    name = StringField("Имя", validators=[DataRequired()])
    email = StringField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_again = PasswordField("Повторите пароль", validators=[DataRequired()])
    about = StringField("Расскажи о себе", validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    sex = StringField('Пол', validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired()])
    submit = SubmitField("Поменять параметры")

