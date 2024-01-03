from rest_framework import routers
from django.urls import path, include
from . views import (DishListView,CategoryViewSet,DishCreateView,SupplierListView,SupplierDetailedView,OrderListView,OrderDetailedView,CreateIngredientViews,SupplierCreateView,DishUpdateView,DishDetailedView,
                     OrderDestroyView,SupplierUpdateView, SupplierDeleteView,IngredientDeleteView,IngredientListView,OrderCreateView,OrderUpdateView,IngredientDetailedView)


router =routers.DefaultRouter()
router.register('category', CategoryViewSet)
urlpatterns = [

    path('ingredient/create/',CreateIngredientViews.as_view(),name='create_ingredient'),
    path('ingredient/',IngredientListView.as_view(),name='ingredient_list'),
    path('ingredient/<int:pk>/',IngredientDetailedView.as_view(),name='ingredient_detail'),
    path('ingredient/<int:pk>/delete/',IngredientDeleteView.as_view(),name='ingredient_delete'),
    path('',include(router.urls)) ,

    # Supplier URLs
    path('supplier/', SupplierListView.as_view(), name='supplier_list'),
    path('supplier/<int:pk>/', SupplierDetailedView.as_view(), name='supplier_detail'),
    path('supplier/create/', SupplierCreateView.as_view(), name='create_supplier'),
    path('supplier/<int:pk>/update/', SupplierUpdateView.as_view(), name='supplier_update'),
    path('supplier/<int:pk>/delete/', SupplierDeleteView.as_view(), name='supplier_delete') ,


      # Dish URLs
    path('dish/', DishListView.as_view(), name='dish_list'),
    path('dish/create/',DishCreateView.as_view(), name='dish_create'),
    path('dish/<int:pk>/', DishDetailedView.as_view(), name='dish_detail'),
    path('dish/<int:pk>/update/', DishUpdateView.as_view(), name='dish_update'),

    # Order URLs
    path('order/create/', OrderCreateView.as_view(), name='create_order'),
    path('order/', OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/', OrderDetailedView.as_view(), name='order_detail'),
    path('order/<int:pk>/delete/', OrderDestroyView.as_view(), name='order_delete'),
    path('order/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),

]