from django.core.management.base import BaseCommand
from homework2.models import Customer, Product


class Command(BaseCommand):
    help = "Create test data"

    def add_arguments(self, parser):
        parser.add_argument('-c', type=int, help='Count of customers')
        parser.add_argument('-p', type=int, help='Count of product')

    def handle(self, *args, **kwargs):
        count_customers = kwargs.get('c')

        if count_customers:
            customers = [
                Customer(
                    name=f"Customer{i}",
                    email=f"customer{i}@mail.com",
                    tel="123456789",
                    address=f"Address of customer{i}",
                )
                for i in range(1, count_customers + 1)
            ]

            for customer in customers:
                customer.save()

            self.stdout.write(f'{customers}')

        count_products = kwargs.get('p')

        if count_products:
            products = [
                Product(
                    name=f"product{i}",
                    description=f"description of product{i}",
                    price=i,
                    count=i
                )
                for i in range(1, count_products + 1)
            ]

            for product in products:
                product.save()

            self.stdout.write(f'{products}')