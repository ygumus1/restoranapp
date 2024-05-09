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
            RestaurantProfile.objects.create(user=user)
        else:
            return JsonResponse({'error': "Invalid account type"}, status=400)


        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})