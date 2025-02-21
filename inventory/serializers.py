from rest_framework import serializers
from users.models import User
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    subtotal = serializers.ReadOnlyField()
    
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'quantity', 'price_at_order', 'subtotal')
        read_only_fields = ('price_at_order',)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_amount = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'created_at', 'updated_at', 'items', 'total_amount')
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            product = item_data.get('product')
            quantity = item_data.get('quantity')
            
            # Check if product has enough stock
            if product.quantity < quantity:
                raise serializers.ValidationError(f"Not enough stock for {product.name}")
            
            # Create order item with current product price
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_order=product.price
            )
            
            # Update product quantity
            product.quantity -= quantity
            product.save()
        
        return order

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('status',)