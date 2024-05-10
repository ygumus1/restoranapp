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
    class Meta:
        model=CustomerProfile
        fields='__all__'

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductCategory
        fields = '__all__'

class RestaurantProfileSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(many=True,read_only=True)
    class Meta:
        model= RestaurantProfile
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    restaurant = RestaurantProfileSerializer(read_only=True)
    category = ProductCategorySerializer(read_only=True)
    class Meta:
        model=Product
        fields='__all__'


class OrderSerializer(serializers.ModelSerializer):
    products=ProductSerializer(many=True,read_only=True)
    restaurant=RestaurantProfileSerializer(read_only=True)
    # customer = CustomerProfileSerializer(read_only=True)
    user = CustomerProfileSerializer(read_only=True)
    
    class Meta:
        model=Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'