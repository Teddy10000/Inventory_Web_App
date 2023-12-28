from django.db import models

# Create your models here.


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=24)
    
class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    Category = models.ForeignKey(Category,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_of_measurement = models.CharField(max_length=40)


    def __str__(self):
        return self.name
    

class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    contact = models.CharField(max_length=40)
    email = models.EmailField(unique=True) 


class Dish(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Ingredient, through='Recipe')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Other fields like description, category, etc.

    def __str__(self):
        return self.name
    
class Order(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    # Other fields like status, delivery date, etc.

    def __str__(self):
        return f"Order {self.id} - {self.supplier.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredient')
    quantity = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    # Other fields related to an individual item within an order

    def __str__(self):
        return f"Order {self.order.id} - {self.ingredient.name} - Qty: {self.quantity}"
