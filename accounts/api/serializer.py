from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework import serializers
from accounts.models import RestaurantProfile,Product,Order,OrderItem,ProductCategory,CustomerProfile

class CustomRegisterSerializer(RegisterSerializer):
    ACCOUNT_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('restaurant', 'Restaurant'),
    )
    account_type = serializers.ChoiceField(choices=ACCOUNT_TYPE_CHOICES)

    def custom_signup(self, request, user):
        user.account_type = self.validated_data.get('account_type', '')
        user.save()

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['account_type'] = self.validated_data.get('account_type', '')
        return data_dict

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
    category = ProductCategorySerializer(many=True, read_only=True)
    products = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantProfile
        fields = '__all__'

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
    

    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'image', 'price', 'restaurant_name']

    def get_restaurant_name(self, obj):
        return obj.restaurant.name if obj.restaurant else None
    
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product_name', 'quantity', 'additional_notes', 'price']  


class OrderSerializer(serializers.ModelSerializer):
    # products=ProductSerializer(many=True,read_only=True)
    order_item = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    restaurant=RestaurantProfileSerializer(read_only=True)
    # user = CustomerProfileSerializer(read_only=True)
    user_name = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model=Order
        # fields = '__all__'
        exclude = ("products", )

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
