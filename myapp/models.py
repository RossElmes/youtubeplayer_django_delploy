from django.db import models
from django.utils import timezone

# Model for Customer
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Model for Product (e.g., different types of coffee, pastries, etc.)
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField('Category', related_name='products', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Model for Variant Category (e.g., Milk, Size)
class VariantCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Model for Product Variant (e.g., oat, dairy, almond)
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    category = models.ForeignKey(VariantCategory, related_name='variants', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    additional_info = models.TextField(blank=True)
    additional_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    @property
    def price(self):
        return self.product.base_price + self.additional_cost

# Model for AddOn (e.g., extra shot, almond milk)
class AddOn(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField('Category', related_name='add_ons', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Model for Category
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Model for Order
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.customer}"

# Model for OrderItem (specific items within an order)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def base_price(self):
        return self.product.base_price

    @property
    def total_price(self):
        variants_total = sum(variant.additional_cost for variant in self.variants.all())
        add_ons_total = sum(item_add_on.total_price for item_add_on in self.add_ons.all())
        return self.quantity * (self.base_price + variants_total) + add_ons_total

# Model for OrderItemVariant (variants applied to an order item)
class OrderItemVariant(models.Model):
    order_item = models.ForeignKey(OrderItem, related_name='variants', on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product_variant.name} for {self.order_item}"

# Model for OrderItemAddOn (specific add-ons within an order item)
class OrderItemAddOn(models.Model):
    order_item = models.ForeignKey(OrderItem, related_name='add_ons', on_delete=models.CASCADE)
    add_on = models.ForeignKey(AddOn, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.add_on.name}"

    @property
    def total_price(self):
        return self.quantity * self.add_on.price
