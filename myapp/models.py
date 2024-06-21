from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Model for Product (e.g., different types of coffee, pastries, etc.)
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'Order {self.id} by {self.customer.username}'

    def update_total_amount(self):
        total_amount = sum(item.product.base_price * item.quantity for item in self.items.all())
        self.total_amount = total_amount
        self.save()

    def confirm_order(self):
        # Call this method when the order is confirmed (e.g., by an admin)
        self.update_total_amount()

    def __str__(self):
        return f"Order {self.id} - {self.customer.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name} (x{self.quantity})'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Do not update total_amount automatically here

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        # Do not update total_amount automatically here
