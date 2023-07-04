categories_data = {
    'clothing': {'cat_id': 'clothing',
                 'cat_title': 'Одежда',
                 'cat_description': 'With supporting text below as a natural lead-in to additional content.'},
    'shoes': {'cat_id': 'shoes',
              'cat_title': 'Обувь',
              'cat_description': 'With supporting text below as a natural lead-in to additional content.'},
    'jackets': {'cat_id': 'jackets',
                'cat_title': 'Куртки',
                'cat_description': 'With supporting text below as a natural lead-in to additional content.'}
}

goods_data = {
    1: {
        'good_id': 1,
        'cat_id': 'clothing',
        'name': 'clothing1',
        'description': 'With supporting text below as a natural lead-in to additional content.',
        'photo_link': '/static/img/product1.webp',
        'price': 100
    },
    2: {
        'good_id': 2,
        'cat_id': 'clothing',
        'name': 'clothing2',
        'description': 'With supporting text below as a natural lead-in to additional content.',
        'photo_link': '/static/img/product2.webp',
        'price': 100
    },
    3: {
        'good_id': 3,
        'cat_id': 'shoes',
        'name': 'shoes3',
        'description': 'With supporting text below as a natural lead-in to additional content.',
        'photo_link': '/static/img/product4.webp',
        'price': 100
    },
    4: {
        'good_id': 4,
        'cat_id': 'shoes',
        'name': 'shoes4',
        'description': 'With supporting text below as a natural lead-in to additional content.',
        'photo_link': '/static/img/product4.webp',
        'price': 100
    },
    5: {
        'good_id': 5,
        'cat_id': 'clothing',
        'name': 'clothing5',
        'description': 'With supporting text below as a natural lead-in to additional content.',
        'photo_link': '/static/img/product3.webp',
        'price': 100
    },
    6: {
        'good_id': 6,
        'cat_id': 'shoes',
        'name': 'shoes6',
        'description': 'With supporting text below as a natural lead-in to additional content.',
        'photo_link': '/static/img/product4.webp',
        'price': 100
    },
    7: {
        'good_id': 7,
        'cat_id': 'clothing',
        'name': 'clothing7',
        'description': 'With supporting text below as a natural lead-in to additional content.',
        'photo_link': '/static/img/product4.webp',
        'price': 100
    }
}


def get_all_categories():
    return categories_data.values()


def get_category_data(category_id):
    return categories_data.get(category_id)


def get_goods_by_category(category_id):
    return list(filter(lambda x: x['cat_id'] == category_id, goods_data.values()))


def get_goods_data(good_id):
    return goods_data.get(good_id)