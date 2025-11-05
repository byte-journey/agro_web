from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from typing import List

class User(AbstractUser):
    ROLES = (
        ('CUSTOMER', 'Customer'),
        ('ADMIN', 'Admin'),
        ('STOCK_MANAGER', 'Stock Manager'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='CUSTOMER')

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("category-view", kwargs={"slug": self.slug})
    

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    class Meta:
        unique_together = ('category', 'slug')
        verbose_name_plural = "SubCategories"

    def __str__(self):
        return f"{self.category.name} → {self.name}"
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='user_cart') # Access user's cart via user.cart
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At') # Automatically set when cart is created
    
    #Hint
    cart_items: models.QuerySet['CartItem']

    @property
    def total_price(self) -> float:
        #Calculate total price of all items in cart
        return sum(item.subtotal for item in self.cart_items.all())
    
    def __str__(self):
        #String representation of cart
        return f"Cart ID: {self.pk}"

# Represents an item in a shopping cart.
# Multiple items can belong to one cart (ForeignKey relationship).
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Product')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Quantity')

    @property
    def subtotal(self) -> float:
        # Calculate the subtotal of the item in the cart (price × quantity)
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
    
    def save(self, *args, **kwargs):
        if self.quantity > self.product.stock:
            raise ValueError("Quantity exceeds available stock")
        super().save(*args, **kwargs)

# Represents a completed order.
# Each order belongs to one user.
class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('F', 'Failed')
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Order Date')
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total Amount')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P', blank=True, verbose_name='Order Status')
    transaction_id = models.CharField(max_length=100, blank=True, verbose_name='Transaction ID')

    # Hint
    order_items: models.QuerySet['OrderItem']
    
    def __str__(self) -> str:
        return f"Order #{self.id} - {self.user.username}" # type: ignore

# Represents an item in a completed order.
# Multiple items can belong to one order.
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.PROTECT, verbose_name='Product')
    quantity = models.PositiveIntegerField(verbose_name='Quantity')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Unit Price')

    @property
    def subtotal(self):
        # Calculate the subtotal of the item in the order (price × quantity)
        return self.price * self.quantity

    def __str__(self) -> str:
        return f"{self.quantity}x {self.product.name} in Order #{self.order}"

    