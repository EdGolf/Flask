from django.core.management.base import BaseCommand
from homework2.models import Customer, Product, Order


class Command(BaseCommand):
    help = "Create new order"

    def add_arguments(self, parser):
        parser.add_argument('order_id', type=int, help='order id')
        parser.add_argument('product_id', type=int, help='product id')

    def handle(self, *args, **kwargs):
        order_id = kwargs.get('order_id')
        product_id = kwargs.get('product_id')
        order = Order.get(order_id)
        product = Product.get(product_id)
        if order is not None and product is not None:
            order.add_product(product)