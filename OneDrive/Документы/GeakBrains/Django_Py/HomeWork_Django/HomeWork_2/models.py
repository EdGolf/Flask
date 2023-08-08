from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    tel = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Customer({self.pk}: {self.name})"

    @staticmethod
    def add(name, email, tel, address):
        new_customer = Customer(name=name, email=email, tel=tel, address=address)
        new_customer.save()
        return new_customer

    @staticmethod
    def get(customer_id):
        customer = Customer.objects.filter(pk=customer_id).first()
        return customer

    @staticmethod
    def get_all():
        customers = Customer.objects.all()
        return list(customers)

    @staticmethod
    def update(customer_id, name=None, email=None, tel=None, address=None):
        customer = Customer.objects.filter(pk=customer_id).first()
        if customer is not None:
            if name:
                customer.name = name
            if email:
                customer.email = email
            if tel:
                customer.tel = tel
            if address:
                customer.address = address
        customer.save()
        return customer

    @staticmethod
    def remove(customer_id):
        customer = Customer.objects.filter(pk=customer_id).first()
        if customer is not None:
            customer.delete()


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Product({self.pk}: {self.name})"

    @staticmethod
    def add(name, description, price, count):
        new_product = Product(name=name, description=description, price=price, count=count)
        new_product.save()
        return new_product

    @staticmethod
    def get(product_id):
        product = Product.objects.filter(pk=product_id).first()
        return product

    @staticmethod
    def get_all():
        products = Product.objects.all()
        return list(products)

    @staticmethod
    def update(product_id, name=None, description=None, price=None, count=None):
        product = Product.objects.filter(pk=product_id).first()
        if product is not None:
            if name:
                product.name = name
            if description:
                product.description = description
            if price:
                product.price = price
            if count:
                product.count = count
        product.save()
        return product

    @staticmethod
    def remove(product_id):
        product = Product.objects.filter(pk=product_id).first()
        if product is not None:
            product.delete()


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Product, related_name="orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order({self.pk}: Customer - {self.customer.name}; Products - {self.products})"

    @staticmethod
    def add(customer):
        new_order = Order(customer=customer)
        new_order.save()
        return new_order

    def add_product(self, product):
        self.products.add(product)
        self.total_amount += product.price
        self.save()

    @staticmethod
    def get(order_id):
        order = Order.objects.filter(pk=order_id).first()
        return order

    @staticmethod
    def get_all():
        orders = Order.objects.all()
        return list(orders)

    @staticmethod
    def remove(order_id):
        order = Order.objects.filter(pk=order_id).first()
        if order is not None:
            order.delete()