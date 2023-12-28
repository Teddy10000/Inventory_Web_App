from . models import Ingredient , Supplier,Order, OrderItem,Dish
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    '''This is the ingredeint serializer responsible for turning the data into json format'''
    class Meta:
        model = Ingredient
        fields = ['id','name','category','quantity','unit_of_measurement']

class CreateIngredientSerializer(serializers.ModelSerializer):
    """Serializer for creating a new ingredients"""

    class Meta:
        model = Ingredient 
        fields = ['id','name','category','quantity','unit_of_measurement']
        read_only_fields = ['id'] 

        def create(self,**validated_data):
            return Ingredient.objects.create(**validated_data)

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id','name','contact','email'] 


class CreateSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier 
        fields = ['id','name','contact','email']
        read_only_fields = ['id'] 

        def create(self,validated_data):
            """Overwriting the create supplier"""
            return Supplier.objects.create(**validated_data)



class DishSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()
    class Meta:
        model = Dish
        fields = ['id','name','price','ingredients'] 

        def get_ingredients(self,obj):
            return IngredientSerializer(obj.items.all(),many=True).data

class DishIngredientSerializer(serializers.Serializer):
    """Serializer for individual dish ingredients."""

    ingredient_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class CreateDishSerializer(serializers.ModelSerializer):
    """The create ingredients serializer that does that has the nested field"""
    ingredients = DishIngredientSerializer(many=True)

    class Meta:
        model = Dish
        fields = ['id','name','price','ingredients']

        def validate_ingredients(self,ingredients):
            for ingredient in ingredients:
                if not ingredient.get('quantity'):
                    raise serializers.ValidationError("Quantity not specified for the given ingredient")
                ingredient_obj = Ingredient.objects.get(pk=ingredient['ingredient'])
                if ingredient['quantity'] > ingredient_obj.quantity:
                    raise serializers.ValidationError("Insufficient quantity of ingredients")
            return ingredients
        def create(self,validated_data):
            ingredient_data = validated_data.pop('ingredients')
            dish = Dish.objects.create(**validated_data)
            dish.ingredients.add(*[Ingredient.objects.get(pk=ingredient['ingredient_id']) for ingredient in ingredient_data]) 

            for ingredients in ingredient_data:
                ingredient = Ingredient.objects.get(pk=ingredient['ingredient_id'])
                ingredient.quantity -= ingredients['quantity'] 
                ingredient.save()
            return dish
            
     

class OrderItemSerializer(serializers.ModelSerializer):
    '''OrderItem seriailizer i need some items explicitly so i have to  like the ingredient making the order item'''
    ingredient_name = serializers.CharField(source='ingredient.name')
    ingredient_price = serializers.IntegerField(source='ingredient.price')
    cost = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = OrderItem
        fields = ('id','ingredient_name','ingredient_price', 'order','quantity','cost')


        def get_costs(self,obj):
            """This gets the cost of by multiplying the objects quantity and objects,ingredients price"""
            return obj.quantity * obj.ingredient.price
      
        def create(self,validated_data):
            """Overwriting the create function to create the orderitem and do the add the ingredints if the already exists o the ingredients"""
            order = validated_data['order']
            ingredient = validated_data['ingredient']
            quantity = validated_data.get('quantity')

            try:
                #First try to get the same Ingredient with same feature
                order_item = OrderItem.objects.get(order=order,ingredient=ingredient)
                if quantity is not None:
                    order_item.quantity += int(quantity)
                    order_item.save()
                    return order_item
                else:
                    return
            except OrderItem.DoesNotExist:
                order_item = OrderItem.objects.create(**validated_data)
                return order_item

class OrderSerializer(serializers.ModelSerializer): 
    '''This is the serializer for the order so when we fetch the order this is how we will see it'''
    ingredients = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ['id','ingredients','supplier','total_cost'] 

        def get_ingredients(self,obj):
            return OrderItemSerializer(obj.items.all(),many=True).data
