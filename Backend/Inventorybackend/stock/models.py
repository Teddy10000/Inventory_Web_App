from django.db import models

# Create your models here.
from django.db import models

class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contact_information = models.JSONField()
    # Other relevant fields (e.g., address, registration details)


class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contact_information = models.JSONField()
    payment_terms = models.CharField(max_length=255)
    lead_time = models.PositiveIntegerField()
    performance_rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contact_information = models.JSONField()
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_terms = models.CharField(max_length=255)
    purchase_history = models.ManyToManyField('SalesOrder')


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, blank=True)
    suppliers = models.ManyToManyField('Supplier')
    attributes = models.JSONField(blank=True)
    unit_of_measure = models.CharField(max_length=255)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_stock_level = models.PositiveIntegerField()
    lead_time = models.PositiveIntegerField()
    reorder_point = models.PositiveIntegerField(blank=True, null=True)
    images = models.ImageField(upload_to='products/', blank=True)
    videos = models.URLField(blank=True)

class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    batch_number = models.CharField(max_length=255, blank=True)
    expiration_date = models.DateField(blank=True, null=True)
    serial_number = models.CharField(max_length=255, blank=True)
    condition = models.CharField(max_length=255, choices=[('NEW', 'New'), ('USED', 'Used'), ('DAMAGED', 'Damaged')], default='NEW')
    purchase_order = models.ForeignKey('PurchaseOrder', on_delete=models.SET_NULL, blank=True, null=True)
    sales_order = models.ForeignKey('SalesOrder', on_delete=models.SET_NULL, blank=True, null=True)
    last_movement_date = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

# TRANSACTIONAL MODELS
class Location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=[('WAREHOUSE', 'Warehouse'), ('STORE', 'Store'), ('SUPPLIER', 'Supplier')])
    address = models.TextField()
    capacity = models.PositiveIntegerField(blank=True, null=True)
    manager = models.ForeignKey('User', on_delete=models.SET_NULL, blank=True, null=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)

class PurchaseOrder(models.Model):
    id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery_date = models.DateField()
    status = models.CharField(max_length=255, choices=[('PENDING', 'Pending'), ('CONFIRMED', 'Confirmed'), ('SHIPPED', 'Shipped'), ('RECEIVED', 'Received')])
    items = models.ManyToManyField('Inventory', through='PurchaseOrderItem')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    payment_terms = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)

class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey('PurchaseOrder', on_delete=models.CASCADE)
    inventory = models.ForeignKey('Inventory', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class SalesOrder(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)

class Report(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255, choices=[('INVENTORY', 'Inventory Report'), ('SALES', 'Sales Report'), ('PURCHASE', 'Purchase Report')])
    date_range = models.CharField(max_length=255)  # Store as a formatted string for flexibility
    filter_criteria = models.JSONField(blank=True)
    generated_data = models.TextField(blank=True)  # Store generated data in text or JSON format
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)

class DemandForecast(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    forecast_date = models.DateField()
    predicted_demand = models.PositiveIntegerField()
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)

class PriceOptimization(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    optimal_price = models.DecimalField(max_digits=10, decimal_places=2)
    calculation_date = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)

class InspectionRecord(models.Model):
    inventory = models.ForeignKey('Inventory', on_delete=models.CASCADE)
    inspection_date = models.DateTimeField(auto_now_add=True)
    inspection_results = models.JSONField()

class WarehouseLayout(models.Model):
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    layout_data = models.JSONField()


