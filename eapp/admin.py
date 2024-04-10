from django.contrib import admin
from .models import Customer, Seller, Category, Subcategory, Product, Order, OrderDetail, Cart, SizeVariant

class SizeVariantInline(admin.TabularInline):
    model = SizeVariant
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = (SizeVariantInline,)

admin.site.register(Customer)
admin.site.register(Seller)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Cart)
