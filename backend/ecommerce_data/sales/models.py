from django.db import models

class Product(models.Model):
    product_id = models.CharField(max_length=50, unique=True)
    product_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.product_name

    class Meta:
        indexes = [models.Index(fields=['category'], name='idx_category')]


class Customer(models.Model):
    customer_id = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.customer_name


class Order(models.Model):
    order_id = models.CharField(max_length=50, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    platform = models.CharField(max_length=100)
    quantity_sold = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_sale_value = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    date_of_sale = models.DateField(db_index=True)
    coupon_used = models.BooleanField(default=False, blank=True, null=True)  # Flipkart-specific
    return_window = models.IntegerField(blank=True, null=True)  # Flipkart-specific
    prime_delivery = models.BooleanField(default=False, blank=True, null=True)  # Amazon-specific
    warehouse_location = models.CharField(max_length=50, blank=True, null=True)  # Amazon-specific
    reseller_name = models.CharField(max_length=255, blank=True, null=True)  # Meesho-specific
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Meesho-specific


    def save(self, *args, **kwargs):
        self.total_sale_value = self.quantity_sold * self.selling_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_id


class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='delivery')
    delivery_address_street = models.CharField(max_length=255)
    delivery_address_city = models.CharField(max_length=100)
    delivery_address_state = models.CharField(max_length=100, db_index=True)
    delivery_address_pin_code = models.CharField(max_length=10)
    delivery_date = models.DateField(db_index=True)
    delivery_status = models.CharField(max_length=20, choices=[('Delivered', 'Delivered'), ('In Transit', 'In Transit'), ('Cancelled', 'Cancelled')], db_index=True)
    delivery_partner = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.order.order_id} - {self.delivery_status}"
