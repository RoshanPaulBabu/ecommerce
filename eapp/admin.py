from django.contrib import admin
from .models import  Customer, Seller, Category, Subcategory, Product, Order, OrderItem
from django.utils.html import format_html
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_no', 'address']
    search_fields = ['name', 'email', 'phone_no']

class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubcategoryInline]

    def get_subcategory_count(self, obj):
        return obj.subcategory_set.count()

    get_subcategory_count.short_description = 'Subcategory Count'

    list_display = ['category_name', 'get_subcategory_count']
    search_fields = ['category_name']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'email', 'contact_number']
    search_fields = ['customer_name', 'email', 'contact_number']
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['display_image','name', 'seller', 'subcategory', 'price', 'quantity_in_stock']
    list_filter = ['seller','subcategory']
    search_fields = ['name']
    def display_image(self, obj):
        return format_html('<img src="{}" width="50px" height="50px" />', obj.image_1.url)

    display_image.short_description = 'Image'
    
    def changelist_view(self, request, extra_context=None):
        # Check stock levels for each product
        for product in Product.objects.all():
            if product.quantity_in_stock < product.reorder_level:
                messages.warning(request, f"Low stock alert: {product.name}")

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)
    
    
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['display_product', 'quantity']
    fields = ['display_product', 'quantity']
    extra = 0

    def display_product(self, obj):
        return format_html('<img src="{}" width="50px" height="50px" /><br>{}', obj.product.image_1.url, obj.product.name)

    display_product.short_description = 'Product'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'address', 'order_date', 'status']
    list_filter = ['status']
    search_fields = ['customer__customer_name']
    inlines = [OrderItemInline]
    readonly_fields = ['id', 'customer', 'address', 'order_date']

    def has_add_permission(self, request):
        return False

    

class InventoryProduct(Product):
    class Meta:
        proxy = True
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventory'

class InventoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity_in_stock', 'reorder_level']
    list_filter = ['seller','subcategory']
    fields = ('quantity_in_stock', 'reorder_level')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in obj._meta.fields if f.name not in ['quantity_in_stock', 'reorder_level']]
    
    def changelist_view(self, request, extra_context=None):
        # Check stock levels for each product
        for product in InventoryProduct.objects.all():
            if product.quantity_in_stock < product.reorder_level:
                messages.warning(request, f"Low stock alert: {product.name}")
                
                # Send email to admin
                send_mail(
                    'Low stock alert',
                    f'The product "{product.name}" is low on stock.',
                    settings.EMAIL_HOST_USER,  # Replace with your email
                    ['roshanpaulbabu007@gmail.com'],  # Replace with admin email
                    fail_silently=False,
                )

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(InventoryProduct, InventoryAdmin)


