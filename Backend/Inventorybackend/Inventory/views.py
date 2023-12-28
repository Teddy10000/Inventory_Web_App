from django.shortcuts import render
from rest_framework import generics, status , permissions
from rest_framework.response import Response
from .models import Ingredient,Supplier,Order,Dish
from . serializers import OrderSerializer
# Create your views here.


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer


    