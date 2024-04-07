from django.contrib import admin
from .models import Customer, Seller, Category, Subcategory, Product, Inventory, Order, OrderDetail, Cart

admin.site.register(Customer)
admin.site.register(Seller)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Cart)
