from django.contrib import admin
from .models import Customer, Seller, Category, Subcategory, Product, Cart, Address, Order, OrderItem



admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Seller)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(Cart)
