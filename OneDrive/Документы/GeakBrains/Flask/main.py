from Flask import Flask, render_template
import database

app = Flask(__name__)


@app.route('/')
@app.route('/index/')
@app.route('/home/')
def index():
    context = {
        'title': 'Главная',
        'categories': database.get_all_categories()
    }
    return render_template('index.html', **context)


@app.route('/categories/<category_id>/')
def categories(category_id):
    context = {
        'categories': database.get_all_categories(),
        'category_data': database.get_category_data(category_id),
        'goods': database.get_goods_by_category(category_id)
    }
    return render_template('categories.html', **context)

@app.route('/goods/<int:good_id>/')
def goods(good_id):
    context = {
        'categories': database.get_all_categories(),
        'good_data': database.get_goods_data(good_id)
    }
    return render_template('goods.html', **context)


if __name__ == '__main__':
    app.run()