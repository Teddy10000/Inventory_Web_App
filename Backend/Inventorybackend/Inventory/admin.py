from django.contrib import admin
from . models import Category, Ingredient , Supplier, Dish ,OrderItem,Order
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display =['id','name','description']

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['id','name','quantity']
    list_filter = ['category']
    search_fields = ['name','description']

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['id','name','contact','email']
    list_filter = ['name','email']
    search_fields = ['name']
