from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='images/user/', blank=True, null=True)
    
    def __str__(self):
        return self.username
    
class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='images/brands/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    class Category(models.TextChoices):
        CAMERAS = 'cameras', 'Camera Bodies'
        LENSES = 'lenses', 'Lenses & Optics'
        STABILIZERS = 'stabilizers', 'Gimbals & Tripods'
        LIGHTING = 'lighting', 'Studio & On-Camera Lighting'
        AUDIO = 'audio', 'Microphones & Audio Recorders'
        STORAGE = 'storage', 'Memory Cards & Drives'
        ACCESSORIES = 'accessories', 'Bags, Power & Rigging'
        
    class Condition(models.TextChoices):
        NEW = 'new', 'Brand New (Sealed)'
        REFURBISHED = 'refurbished', 'Factory Refurbished'
        OPEN_BOX = 'open_box', 'Open Box / Mint'

    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=Category.choices)
    condition = models.CharField(max_length=20, choices=Condition.choices, default=Condition.NEW)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    product_image = models.ImageField(upload_to='images/products/')
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True, help_text="Unique Product SKU Stock Identifier")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_new_arrival(self):
        return self.created_at >= timezone.now() - timedelta(days=7)
    
    @property
    def average_rating(self):
        avg_rating = self.reviews.aggregate(avg_rating=models.Avg('rating'))['avg_rating']
        return round(avg_rating, 1) if avg_rating else 0.0

    def __str__(self):
        return f"[{self.brand.name if self.brand else 'Generic'}] {self.name}"
    
class Wishlist(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    class Status(models.TextChoices):
        PAID = 'paid', 'Payment Confirmed'
        SHIPPING = 'shipping', 'In Transit'
        DELIVERED = 'delivered', 'Delivered'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PAID)
    transaction_id = models.CharField(max_length=100, help_text="Payment provider tracking reference ID")
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def item_count(self):
        return self.items.aggregate(total=models.Sum('quantity'))['total'] or 0

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_price(self):
        return self.price_at_purchase * self.quantity

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)