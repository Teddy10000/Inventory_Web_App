from rest_framework import routers
from django.urls import path, include
from . views import (DishListView,CreateIngredientViews,SupplierCreateView,DishUpdateView,DishDetailedView,
                     OrderDestroyView,SupplierUpdateView,OrderCreateView,OrderUpdateView,IngredientDetailedView)



urlpatterns = [

    path('ingredient/create/',CreateIngredientViews.as_view,name='create_ingredient'),
    path()
]