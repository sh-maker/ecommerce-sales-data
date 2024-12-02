from django.contrib import admin
from .models import Product, Customer, Order, Delivery


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'category')
    search_fields = ('product_id', 'product_name', 'category')
    list_filter = ('category',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'customer_name', 'contact_email', 'phone_number')
    search_fields = ('customer_id', 'customer_name', 'contact_email', 'phone_number')
    list_filter = ('contact_email',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'platform', 'product', 'customer', 'quantity_sold', 'selling_price', 'date_of_sale')
    search_fields = ('order_id', 'platform', 'product__product_name', 'customer__customer_name')
    list_filter = ('platform', 'date_of_sale', 'product__category')
    ordering = ('-date_of_sale',)
    fieldsets = (
        (None, {
            'fields': ('order_id', 'product', 'customer', 'platform', 'quantity_sold', 'selling_price', 'date_of_sale'),
        }),
        ('Platform-Specific Fields', {
            'fields': ('coupon_used', 'return_window', 'prime_delivery', 'warehouse_location', 'reseller_name', 'commission_percentage'),
        }),
    )


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('order', 'delivery_date', 'delivery_status', 'delivery_address_street', 'delivery_address_city', 'delivery_address_state', 'delivery_address_pin_code')
    search_fields = ('order__order_id', 'delivery_status', 'delivery_address_city', 'delivery_address_state', 'delivery_address_pin_code')
    list_filter = ('delivery_status', 'delivery_date', 'delivery_address_state')
    ordering = ('-delivery_date',)
