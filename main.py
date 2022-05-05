from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
import os
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_uploads import patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from flask_login import login_user, login_required, logout_user, LoginManager
from forms.register_form import RegisterForm, LoginForm, ChangeForm



app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads')
login_manager = LoginManager()
login_manager.init_app(app)

#https://docs-python.ru/packages/veb-frejmvork-flask-python/zagruzka-fajlov-server-flask/
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
# максимальный размер файла, по умолчанию 16MB
patch_request_class(app)

class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, 'Image only!'),
                      FileRequired('File was empty!')])
    submit = SubmitField("Зарегистрироваться")

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

@app.route('/register1/<file_name>', methods=['GET', 'POST'])
def reqister(file_name):
    form = RegisterForm()
    print('register')
    if form.validate_on_submit():
        print('if')
        if form.password.data != form.password_again.data:
            print('Пароли не совпадают')
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")

        db_sess = db_session.create_session()
        User.photo = file_name
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
            photo = 'uploads/'+file_name
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
            return redirect(f'/main_page/{user.email}')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    print('return submit')
    return render_template('login.html', title='Загрузите каринку', form=form)


@app.route('/main_page/<email>', methods=['GET', 'POST'])
def main_page(email):
    db_sess = db_session.create_session()
    users = db_sess.query(User)
    return render_template("main_page.html", users=users, email=email)

@app.route('/register', methods=['GET', 'POST'])
def upload_file():
    print('попытка откыь ')
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        return redirect(f'/register1/{filename}')
    else:
        file_url = None
    print('db ses')

    return render_template('save_picture.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/change_params/<email>', methods=['GET', 'POST'])
def change_params(email):
    form = ChangeForm()
    print('Change')
    if form.validate_on_submit():
        print('if')
        if form.password.data != form.password_again.data:
            print('Пароли не совпадают')
            return render_template('change_params.html', title='Cмена параетров аккаунта',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == email).first()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            print("Такой пользователь уже есть")
            return render_template('change_params.html', title='Cмена параетров аккаунта',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if user.check_password(form.password.data):
            print('Неверный старый пароль')
            return render_template('change_params.html', title='Cмена параетров аккаунта',
                                   form=form,
                                   message="Пароли не совпадают")
        user.email = form.name.data
        user.name = form.name.data
        user.age = form.age.data
        user.sex = form.sex.data
        user.city = form.city.data
        user.about = form.about.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        print('по идее сэйв')
        return redirect('/login')
    print('return')
    return render_template('change_params.html', title='Cмена параетров аккаунта', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    db_sess = db_session.create_session()
    users = db_sess.query(User)
    return render_template("profile.html", users=users)

if __name__ == '__main__':
    main()