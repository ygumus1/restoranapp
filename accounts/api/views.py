from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.http import JsonResponse
from accounts.models import CustomerProfile, RestaurantProfile
from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404
from accounts.models import RestaurantProfile,CustomerProfile,ProductCategory,Order,OrderItem,Product,User
from accounts.api.serializer import CustomerProfileSerializer,ProductCategorySerializer,OrderSerializer,OrderItemSerializer,ProductSerializer,RestaurantProfileSerializer

class CustomerProfileAPIView(generics.ListCreateAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class CustomerProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductCategoryAPIView(generics.ListCreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductCategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class RestaurantProfileAPIView(generics.ListCreateAPIView):
    queryset = RestaurantProfile.objects.all()
    serializer_class = RestaurantProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class RestaurantProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RestaurantProfile.objects.all()
    serializer_class = RestaurantProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    

class ProductAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes =[permissions.IsAuthenticated]

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes =[permissions.IsAuthenticated]




### Login
class LoginView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)
        
### Register
from dj_rest_auth.registration.views import RegisterView as DefaultRegisterView
from accounts.api.serializer import CustomRegisterSerializer

class RegisterView(DefaultRegisterView):
    permission_classes = [AllowAny]
    serializer_class = CustomRegisterSerializer

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        account_type = request.data.get('account_type')

        if User.objects.filter(username__iexact=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        if User.objects.filter(email__iexact=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)
        if password1 != password2:
            return JsonResponse({'error': "Passwords don't match"}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password1)


        if account_type == 'customer':
            CustomerProfile.objects.create(user=user)
        elif account_type == 'restaurant':
            # adress = request.data["adress"]
            # x = RestaurantProfile.objects.create(
            #     adress = request.data["adress"],
            # )
            RestaurantProfile.objects.create(user=user)

    
        else:
            return JsonResponse({'error': "Invalid account type"}, status=400)


        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})