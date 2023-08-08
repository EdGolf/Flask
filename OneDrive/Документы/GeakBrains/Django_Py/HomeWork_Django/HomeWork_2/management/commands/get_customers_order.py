from django.core.management.base import BaseCommand
from homework2.models import Customer, Order


class Command(BaseCommand):
    help = "Create new order"

    def add_arguments(self, parser):
        parser.add_argument('customer_id', type=int, help='customers id')

    def handle(self, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        customer = Customer.get(customer_id)
        if customer is not None:
            orders = customer.orders.all()
            self.stdout.write(f'{orders}')