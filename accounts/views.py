from django.shortcuts import render
from rest_framework import generics
# from dj_rest_auth.views import PasswordResetView
# from dj_rest_auth.serializers import PasswordResetSerializer
# Create your views here.
class OrderView(generics.ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        print(request.data)
        return self.list(request, *args, **kwargs)
    