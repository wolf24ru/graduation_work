from rest_framework import serializers

from product.serializers import ProductInfoINSerializer
from accounts.serializers import ContactSerializer
from order.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    cost_one = serializers.FloatField(required=False)

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'product_info', 'quantity', 'cost_one')
        read_only_fields = ('id', 'cost_one')
        extra_kwargs = {
            'order': {'write_only': True}
        }


class OrderItemGetSerializer(OrderItemSerializer):
    product_info = ProductInfoINSerializer(read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemGetSerializer(read_only=True, many= True)
    total_sum = serializers.FloatField()
    contact = ContactSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'status', 'order_items', 'date', 'total_sum', 'contact')
        read_only_fields = ('id',)


class OrderItemAddQuantitySerializer(OrderItemSerializer):
    id = serializers.IntegerField(read_only=True)
    quantity = serializers.IntegerField(required=True)
