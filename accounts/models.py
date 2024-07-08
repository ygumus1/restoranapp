from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefon = models.CharField(max_length=11)
    adres = models.TextField()
    account_type= models.CharField(default="Customer",max_length=20)

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
    categories = models.ManyToManyField(ProductCategory, related_name="restaurants")
    account_type= models.CharField(default="Restaurant",max_length=20)


    def __str__(self):
        return self.name + "'s Profile"


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE, null=True, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.BooleanField(default=False)
    order_note = models.TextField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.pk} by {self.user.user.username} at {self.restaurant.name}"

    def get_total_price(self):
        total = sum(item.product.price * item.quantity for item in self.order_items.all())
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    additional_notes = models.TextField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Order #{self.order.pk}"


        
    

