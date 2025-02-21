from rest_framework import serializers
from django.db import transaction, IntegrityError
from django.db.models import F
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
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'created_at', 'updated_at', 'items', 'total_amount')

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user

        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            product_data = item_data.get('product')
            quantity = item_data.get('quantity')  # Define quantity here!

            product_id = None

            if isinstance(product_data, Product):
                product_id = str(product_data.id)
            elif isinstance(product_data, str):
                product_id = product_data
            else:
                raise serializers.ValidationError("Invalid product data. Must be a UUID string or a Product object.")

            try:
                updated_rows = Product.objects.filter(pk=product_id, quantity__gte=quantity).update(quantity=F('quantity') - quantity)

                if updated_rows == 0:
                    raise serializers.ValidationError(f"Not enough stock for product with id {product_id}")

                product = Product.objects.get(pk=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price_at_order=product.price
                )
            except IntegrityError:
                raise serializers.ValidationError(f"Not enough stock for product with id {product_id}")
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with id {product_id} not found")
            except serializers.ValidationError as e:
                transaction.rollback()
                raise e

        return order

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('status',)