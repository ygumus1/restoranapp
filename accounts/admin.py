from django.contrib import admin
from .models import RestaurantProfile, CustomerProfile, Order, OrderItem, ProductCategory, Product

admin.site.register(RestaurantProfile)
admin.site.register(CustomerProfile)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(ProductCategory)