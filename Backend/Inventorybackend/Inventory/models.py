from django.db import models

# Create your models here.

class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
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
    ingredients = models.ManyToManyField(Ingredient)
    order_date = models.DateField(auto_now_add=True)
    # Other fields like status, delivery date, etc.

    def __str__(self):
        return f"Order {self.id} - {self.supplier.name}"

