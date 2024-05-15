from django.urls import path
from accounts.api import views as api_views

urlpatterns = [
    path('costomer-profile/',api_views.CustomerProfileAPIView.as_view(),name='customer-profil'),
    path('costomer-profile/<int:pk>',api_views.CustomerProfileDetailAPIView.as_view(),name='customer-profil-detail'),
    path('category/',api_views.ProductCategoryAPIView.as_view(),name='product-category'),
    path('category/<int:pk>',api_views.ProductCategoryDetailAPIView.as_view(),name='product-category-detail'),
    path('orders/',api_views.OrderView.as_view(),name='orders'),
    path('orders/<int:pk>',api_views.SingleOrderView.as_view(),name='orders-detail'),
    path('restaurants',api_views.RestaurantProfileAPIView.as_view(),name='restaurants'),
    path('restaurants/<int:pk>',api_views.RestaurantProfileDetailAPIView.as_view(),name='restoranlar-detail'),
    path('product/',api_views.ProductListAPIView.as_view(),name='product'),
    path('product/<int:pk>',api_views.ProductDetailAPIView.as_view(),name='product-detail'),
    path('product/create',api_views.ProductCreateAPIView.as_view(),name='product-create'),
]