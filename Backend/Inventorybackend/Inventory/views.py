from django.shortcuts import render
from rest_framework import generics, status , permissions
from rest_framework.response import Response
from .models import Ingredient,Supplier,Order,Dish
from django.db.models import F

from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from . serializers import OrderSerializer,OrderItemSerializer , CreateSupplierSerializer, UpdateDishSerializer,DishIngredientSerializer,DishSerializer,SupplierSerializer,IngredientSerializer,CreateIngredientSerializer
# Create your views here.
from rest_framework import serializers
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

class IngredientDeleteView(generics.DestroyAPIView):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    lookup_field = 'pk'



class SupplierListView(generics.ListAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class SupplierRetrieveView(generics.RetrieveAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    lookup_field = 'pk'

class SupplierCreateView(generics.CreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = CreateSupplierSerializer

class SupplierUpdateView(generics.UpdateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class DishListView(generics.ListAPIView):
    serializer_class = DishSerializer
    queryset = Dish.objects.all()   

class DishDetailedView(generics.RetrieveAPIView):
    """Queryset used to show what the view can have access to"""
    serializer_class = DishSerializer
    queryset = Dish.objects.all()

class DishUpdateView(generics.UpdateAPIView):
    """Update a specific dish object."""

    queryset = Dish.objects.all()  # Adjust queryset if needed
    serializer_class = UpdateDishSerializer
    permission_classes = [permissions.IsAuthenticated]  # Example permission


class DishDetailedView(generics.RetrieveAPIView):
    serializer_class = DishSerializer

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes =[permissions.IsAuthenticated]

    @transaction.atomic
    def create_order(order_data):
        """Creates an order and updates ingredient quantities before saving."""
        try:
            for item_data in order_data['order_items']:
                ingredient = Ingredient.objects.select_for_update().get(pk=item_data['ingredient_id'])
                ingredient.quantity += item_data['quantity']
                ingredient.save()
        except Exception as e:
             transaction.set_rollback(True)
             raise serializers.ValidationError("Order creation failed: {}".format(str(e))) from e

    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = self.create_order(serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED, headers=headers)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes =[permissions.IsAuthenticated]


  
class OrderDetailedView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = 'pk'
    permission_classes =[permissions.IsAuthenticated]

class OrderDestroyView(generics.DestroyAPIView):
    """FOR THE ORDER DELETE VIEW"""
    serializer_class = OrderSerializer  # You might not need a serializer here
    queryset = Order.objects.all()
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def destroy(self,request,*args,**kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def perform_destroy(self,instance):
        for item in instance.items.all():
            ingredient = item.ingredient
            ingredient.quantity -= item.quantity
            ingredient.save()
        instance.delete()

class OrderUpdateView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = 'pk'
    
    @transaction.atomic
    def perform_update(self,serializer):
        order = serializer.save()

        #updating ingredient quantities based on changes in order items
        for item in order.items.all():
            ingredient = item.ingredient
            old_quantity = getattr(serializer.instance.items.get(pk=item.pk), 'quantity', 0)  # Get old quantity
            ingredient.quantity = F('quantity') - old_quantity + item.quantity
            ingredient.save()





    