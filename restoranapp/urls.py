"""
URL configuration for restoranapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.api.views import CustomerRegisterView,RestaurantRegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('accounts.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('dj-rest-auth/registration/', RegisterView.as_view(), name='rest_register'),
    path('dj-rest-auth/registration/customer', CustomerRegisterView.as_view(), name='customer_rest_register'),
    path('dj-rest-auth/registration/restoran', RestaurantRegisterView.as_view())
]
