from django.db import models
from django.contrib.auth.models import User

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefon = models.CharField(max_length=11)
    adres = models.TextField()

    def __str__(self):
        return self.user.username + "'s Profile"
    
class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class RestaurantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    image = models.ImageField(upload_to='restaurants/')
    minimum_order_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    category = models.ManyToManyField(ProductCategory,related_name="categories_in_restaurants" )

    def __str__(self):
        return self.name + "'s Profile"


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(Product, through='OrderItem')
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}'s order to {self.restaurant.name} restaurant"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    additional_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} for {self.order.user.username}"
