from flask import Flask, render_template, request, redirect, make_response, url_for, abort, flash, session
from .models import db, User
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task2_data.db'
db.init_app(app)
app.config['SECRET_KEY'] = 'impossibletoknow'


@app.cli.command("init-db")
def init_db():
    db.drop_all()
    db.create_all()
    print('OK')


@app.cli.command("fill-db")
def fill_db():
    first_user = User(
        nickname="vasya",
        firstname="Вася",
        lastname="Пупкин",
        email="pupkin@mail.com",
        birth_date=datetime(2000, 1, 1, 0, 0, 0),
        psw_hash=generate_password_hash('abc123456')
    )
    db.session.add(first_user)
    db.session.commit()


@app.route('/')
@app.route('/index/')
def index():
    context = {
        'title': 'Главная',
    }
    return render_template('index.html', **context)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        session['new_user'] = {
            'nickname': form.nickname.data,
            'firstname': form.firstname.data,
            'lastname': form.lastname.data,
            'email': form.email.data,
            'birth_date_year': form.birth_date.data.year,
            'birth_date_month': form.birth_date.data.month,
            'birth_date_day': form.birth_date.data.day,
            'psw_hash': generate_password_hash(form.password.data)
        }
        return redirect(url_for('register_confirm', action='ask'))

    context = {
        'title': 'Регистрация',
        'form': form
    }
    return render_template('register.html', **context)


@app.route('/register/confirm/<action>')
def register_confirm(action):
    if new_user := session.get('new_user'):
        match action:
            case 'ask':
                context = {
                    'title': 'Регистрация',
                    'new_user': new_user
                }
                return render_template('register_conf.html', **context)
            case 'confirm':
                user = User(
                    nickname=new_user['nickname'],
                    firstname=new_user['firstname'],
                    lastname=new_user['lastname'],
                    email=new_user['email'],
                    birth_date=datetime(new_user['birth_date_year'], new_user['birth_date_month'],
                                        new_user['birth_date_day']),
                    psw_hash=new_user['psw_hash'])
                db.session.add(user)
                db.session.commit()
                session.pop('new_user')
                flash('Пользователь зарегистрирован', 'success')
            case 'cancel':
                session.pop('new_user')
                flash('Регистрация отменена', 'danger')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()