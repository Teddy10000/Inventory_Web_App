from rest_framework import serializers

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

class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = PurchaseOrderItemSerializer(many=True)

    class Meta:
        model = PurchaseOrder
        fields = (
            'id',
            'supplier',  # Include nested supplier details for reference
            'order_date',
            'expected_delivery_date',
            'status',
            'items',
            'total_cost',
        )
