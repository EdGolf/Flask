from flask import Flask, render_template, request, redirect, make_response, url_for, abort
import database

app = Flask(__name__)


@app.route('/')
@app.route('/index/')
def index():
    context = {
        'title': 'Главная',
        'username': request.cookies.get('username')
    }
    return render_template('index.html', **context)


@app.post('/login/')
def login_post():
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('username', request.form.get('username'))
    response.set_cookie('email', request.form.get('email'))
    return response


@app.get('/login/')
def login_get():
    context = {
        'title': 'Авторизация',
        'username': request.cookies.get('username')
    }
    return render_template('login.html', **context)


@app.route('/logout/')
def logout():
    response = make_response(redirect(url_for('login_get')))
    response.delete_cookie('username')
    response.delete_cookie('email')
    return response


@app.route('/hello/')
def hello():
    context = {
        'title': 'Привет',
        'username': request.cookies.get('username')
    }
    return render_template('hello.html', **context)


@app.get('/pow2/')
def pow2_get():
    context = {
        'title': 'Привет',
        'username': request.cookies.get('username')
    }
    return render_template('pow2_form.html', **context)


@app.post('/pow2/')
def pow2_post():
    try:
        num = float(request.form.get('number'))
    except ValueError:
        abort(500)

    return redirect(url_for('show_result', number=num, result=num ** 2))


@app.route('/show_result/')
def show_result():
    context = {
        'title': 'Результат',
        'username': request.cookies.get('username'),
        'number': request.args.get('number'),
        'result': request.args.get('result')
    }
    return render_template('show_result.html', **context)


@app.errorhandler(500)
def error500(e):
    context = {
        'title': 'Ошибка сервера',
        'username': request.cookies.get('username'),
    }
    return render_template('500.html', **context)


@app.errorhandler(404)
def error404(e):
    context = {
        'title': 'Ошибка сервера',
        'username': request.cookies.get('username'),
    }
    return render_template('404.html', **context)


if __name__ == '__main__':
    app.run()