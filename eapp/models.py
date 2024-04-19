from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinLengthValidator

class Address(models.Model):
    recepient_name = models.CharField(max_length=100, null=True)
    recepient_contact = models.CharField(max_length=12, null=True, validators=[MinLengthValidator(10)])
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.address_line1}, {self.address_line2}, {self.city}, {self.state} - {self.postal_code}"    

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    customer_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=12, blank=True, null=True, validators=[MinLengthValidator(10)])
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, default='customer')

    def __str__(self):
        return self.customer_name
   
    

class Seller(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=12, unique=True, validators=[MinLengthValidator(10)])
    address = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.category_name

class Subcategory(models.Model):
    subcategory_name = models.CharField(max_length=100)
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.subcategory_name

class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_1 = models.ImageField(upload_to='product_images/')
    image_2 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name



class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def sub_total(self):
        return int(self.product.price) * int(self.quantity)

    def __str__(self):
        return f"Cart - Customer: {self.customer.customer_name} - Product: {self.product.name} - Qty: {self.quantity}"
    
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped/Dispatched', 'Shipped/Dispatched'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Refunded', 'Refunded'),
        ('Returned', 'Returned'),
        ('On Hold', 'On Hold'),
        ('Backordered', 'Backordered'),
        ('Partially Shipped', 'Partially Shipped'),
        ('Awaiting Payment', 'Awaiting Payment'),
        ('Awaiting Fulfillment', 'Awaiting Fulfillment'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def total_price(self):
        return sum(item.total_price() for item in self.orderitem_set.all())

    def __str__(self):
        return f"Order - Customer: {self.customer.customer_name} - Status: {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"Order Item - Order: {self.order.id} - Product: {self.product.name} - Qty: {self.quantity}"
