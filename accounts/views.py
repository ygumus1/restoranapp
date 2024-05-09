from django.shortcuts import render
from rest_framework import generics
# Create your views here.
class OrderView(generics.ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        print(request.data)
        return self.list(request, *args, **kwargs)
    