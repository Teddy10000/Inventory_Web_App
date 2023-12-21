from django.db import models

# Create your models here.

class Ingredients(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    quantity = models.IntegerField()
    unit_of_measurement = models.CharField(max_length=40)

