from django.shortcuts import render
from rest_framework import generics, status , permissions
from rest_framework.response import Response
from .models import Ingredient,Supplier,Order,Dish
from . serializers import OrderSerializer, CreateSupplierSerializer, DishIngredientSerializer,DishSerializer,SupplierSerializer,IngredientSerializer,CreateIngredientSerializer
# Create your views here.

class CreateIngredientViews(generics.CreateAPIView):
    serializer_class = CreateIngredientSerializer
    queryset = Ingredient.objects.all()

class IngredientListView(generics.ListAPIView):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

class IngredientDetailedView(generics.RetrieveAPIView):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    lookup_field = 'pk'


class SupplierListView(generics.ListAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class SupplierRetrieveView(generics.RetrieveAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class SupplierCreateView(generics.CreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = CreateSupplierSerializer

class SupplierUpdateView(generics.UpdateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer



    