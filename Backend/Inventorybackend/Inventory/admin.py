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

class IngredientInline(admin.TabularInline):
    model = Ingredient

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['id','name','contact','email']
    list_filter = ['name','email']
    search_fields = ['name']


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'description']  # Add more fields as needed
    search_fields = ['name', 'description']
    inlines = [IngredientInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'total_price', 'created_at']  # Add more fields as needed
    list_filter = ['created_at']
    search_fields = ['customer_name']