from rest_framework import serializers
from . models import Inventory,PurchaseOrder,PurchaseOrderItem,Product,Customer,Organization

from rest_framework import serializers
from .models import Customer, SalesOrder

class SalesOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrder
        fields = '__all__'  # Include all fields of SalesOrder

class CustomerSerializer(serializers.ModelSerializer):
    purchase_history = SalesOrderSerializer(many=True, read_only=True, source='salesorder_set')

    class Meta:
        model = Customer
        fields = ('id', 'name', 'contact_information', 'credit_limit', 'payment_terms', 'purchase_history')



from .models import Supplier

class SupplierCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('name', 'contact_information', 'payment_terms', 'lead_time')


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('name', 'contact_information', 'payment_terms', 'lead_time')


class SupplierListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('id', 'name', 'performance_rating')  # Adjusted fields for listing


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = (
            'id',
            'product',  # Include nested product details for reference
            'location',  # Include nested location details for clarity
            'quantity',
            'batch_number',
            'expiration_date',
            'condition',
        )

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'sku',
            'category',  # Include nested category details for clarity
            'brand',  # Include nested brand details if applicable
            'unit_of_measure',
            'retail_price',
            'min_stock_level',
            'available_stock',  # Calculate available stock from Inventory model
        )

    available_stock = serializers.SerializerMethodField()

    def get_available_stock(self, obj):
        return obj.inventory_set.aggregate(total_stock=models.Sum('quantity'))['total_stock']

class PurchaseOrderItemSerializer(serializers.ModelSerializer): 
    #PRODUCT HERE BECAUSE OF THE RELATIONSHIP WITH INVENTORY
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    supplier = SupplierSerializer(read_only=True)  # Nested supplier details

    class Meta:
        model = PurchaseOrderItem
        fields = (
            'id',
            'product',
            'quantity',
            'unit_price',
            'line_total',
            'supplier',  # Include nested supplier
        )
class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = PurchaseOrderItemSerializer(many=True)

    class Meta:
        model = PurchaseOrder
        fields = ('id', 'supplier', 'order_date', 'expected_delivery_date', 'status', 'items', 'total_cost', 'payment_terms', 'notes', 'organization')


    def update_supplier_status(supplier, purchase_order_status):
        if purchase_order_status == 'PENDING':
            supplier.has_pending_orders = True
        elif purchase_order_status == 'CONFIRMED':
            supplier.confirmed_orders_count += 1
        elif purchase_order_status == 'SHIPPED':
            supplier.shipped_orders_count += 1
        elif purchase_order_status == 'RECEIVED':
            supplier.completed_orders_count += 1
            # Calculate on-time delivery rate (adjust logic as needed)
            supplier.on_time_delivery_rate = supplier.completed_orders_count / supplier.shipped_orders_count
        else:
            # Handle unexpected status appropriately
            raise ValueError(f"Invalid purchase order status: {purchase_order_status}")

        supplier.save()
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        purchase_order = PurchaseOrder.objects.create(**validated_data)

        with transaction.atomic():  # Ensure data integrity
            for item_data in items_data:
                inventory = Inventory.objects.get(id=item_data['inventory_id'])
                if purchase_order.status == 'PENDING':
                    inventory.expected_quantity += item_data['quantity']
                    inventory.save()
                    # Optionally consider reserving expected quantities here
                PurchaseOrderItem.objects.create(purchase_order=purchase_order, **item_data)

            self.update_supplier_status(purchase_order.supplier, purchase_order.status)

        return purchase_order

    def update(self, instance, validated_data):
        # Handle inventory and supplier updates based on status changes
        # ... (implementation details for update logic)

        with transaction.atomic():
            old_status = instance.status
            new_status = validated_data.get('status',old_status)
            instance = super().update(instance,validated_data)

            #Handle inventory updates based on status changes

            if new_status == "PENDING" and old_status != "PENDING":
                for item in instance.items.all():
                    inventory = item.inventory 
                    inventory.expected_quantity += item.quantity
                    inventory.save()
            elif new_status == "RECEIVED" and old_status != "RECEIVED":
                for item in instance.items.all():
                    inventory = item.inventory
                    inventory.quantity += item.quantity
                    inventory.expected_quantity -= item.quantity
                    inventory.save()
            self.update_supplier_status(instance.supplier,status)


            


