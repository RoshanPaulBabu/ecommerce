from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    recepient_name = models.CharField(max_length=100, null=True)
    recepient_contact = models.CharField(max_length=20, null=True)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.address_line1}, {self.address_line2}, {self.city}, {self.state} - {self.postal_code}"    

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    customer_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=50, default='customer')

    def __str__(self):
        return self.customer_name   
    

class Seller(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=12, unique=True)
    address = models.CharField(max_length=255)

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

class Subcategory(models.Model):
    subcategory_name = models.CharField(max_length=100)
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_in_stock = models.IntegerField()
    reorder_level = models.IntegerField()

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.CharField(max_length=255)
    status = models.CharField(max_length=50)

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()