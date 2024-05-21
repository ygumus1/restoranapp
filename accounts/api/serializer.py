from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from accounts.models import RestaurantProfile,Product,Order,OrderItem,ProductCategory,CustomerProfile
from django.contrib.auth.models import User

# class CustomRegisterSerializer(RegisterSerializer):
#     ACCOUNT_TYPE_CHOICES = (
#         ('customer', 'Customer'),
#         ('restaurant', 'Restaurant'),
#     )
#     account_type = serializers.ChoiceField(choices=ACCOUNT_TYPE_CHOICES)

#     def custom_signup(self, request, user):
#         user.account_type = self.validated_data.get('account_type', '')
#         user.save()

#     def get_cleaned_data(self):
#         data_dict = super().get_cleaned_data()
#         data_dict['account_type'] = self.validated_data.get('account_type', '')
#         return data_dict

class CustomerRegisterSerializer(RegisterSerializer):
    adres = serializers.CharField()
    telefon=serializers.CharField()
    def custom_signup(self, request, user):
        user.save()

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        return data_dict
    
class RestaurantRegisterSerializer(RegisterSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    name = serializers.CharField()
    address = serializers.CharField()
    image = serializers.ImageField()
    minimum_order_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    category = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all(), many=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'name', 'address', 'image', 'minimum_order_amount', 'category']

    def create(self, validated_data):
        user_data = {key: validated_data.pop(key) for key in ['username', 'password', 'email']}
        user = User.objects.create_user(**user_data)
        RestaurantProfile.objects.create(user=user, **validated_data)
        return user
    
##########################

class CustomerProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model=CustomerProfile
        fields='__all__'

    def get_user(self, obj):
        return obj.user.username if obj.user else None

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductCategory
        fields = '__all__'

class RestaurantProfileSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantProfile
        # fields = '_all_'
        fields = ['id', 'products', 'name', 'address', 'image', 'minimum_order_amount', 'user', 'categories']

    def get_categories(self, obj):
        # Kategori isimlerini döndüren bir yöntem
        return [category.name for category in obj.categories.all()]

    def get_products(self, obj):
        products = Product.objects.filter(restaurant=obj)
        product_data = []
        for product in products:
            product_data.append({
                'name': product.name,
                'description': product.description,
                'price': product.price,
                # 'image': product.image,
                'category': product.category.name,
                'image': product.image.url
            })
        return product_data

class ProductSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    

    class Meta:
        model = Product
        fields = ['name', 'category_name', 'description', 'image', 'price', 'restaurant_name']

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
    def get_restaurant_name(self, obj):
        return obj.restaurant.name if obj.restaurant else None
    
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product_name', 'quantity', 'additional_notes', 'price']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)  # Değişiklik burada, source kullanmaya gerek yok
    user_name = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'order_items', 'user', 'user_name', 'total_price']

    def get_user_name(self, obj):
        return obj.user.user.username

    def get_user(self, obj):
        return {
            'id': obj.user.user.id,
            'telefon': obj.user.telefon,
            'adres': obj.user.adres,
            'username': obj.user.user.username
        }

    def get_total_price(self, obj):
        return obj.get_total_price()

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for order_item_data in order_items_data:
            OrderItem.objects.create(order=order, **order_item_data)
        return order