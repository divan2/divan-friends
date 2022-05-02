from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from flask_login import login_user, login_required, logout_user
from forms.register_form import RegisterForm, LoginForm
from data.db_session import global_init, create_session
app = Flask(__name__)
from flask_login import LoginManager
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

def main():
    db_session.global_init("db/blogs.db")
    app.run()

@app.route("/")
def index():
    return render_template("base.html", title="Главная страница")

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    print('register')
    if form.validate_on_submit():
        print('if')
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        print('Пароли не совпадают')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            print("Такой пользователь уже есть")
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data,
            sex=form.sex.data,
            age=form.age.data,
            city=form.city.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        print('по идее сэйв')
        return redirect('/login')
    print('return')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print('login')
    if form.validate_on_submit():
        print('if')
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            print('if user')
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    print('return submit')
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

if __name__ == '__main__':
    main()