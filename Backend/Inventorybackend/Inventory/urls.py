from rest_framework import routers
from django.urls import path, include
from . views import (DishListView,CreateIngredientViews,SupplierCreateView,DishUpdateView,DishDetailedView,
                     OrderDestroyView,SupplierUpdateView,IngredientDeleteView,IngredientListView,OrderCreateView,OrderUpdateView,IngredientDetailedView)



urlpatterns = [

    path('ingredient/create/',CreateIngredientViews.as_view,name='create_ingredient'),
    path('ingredient/',IngredientListView.as_view,name='ingredient_list'),
    path('ingredient/<int:pk>/',IngredientDetailedView.as_view,name='ingredient_detail'),
    path('ingredient/<int:pk>/delete/',IngredientDeleteView.as_view,name='ingredient_')

]