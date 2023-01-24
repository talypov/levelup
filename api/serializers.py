from django_celery_results.models import TaskResult
from rest_framework import serializers
from product.models import Product, Order


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'id',
            'product_no',
            'name',
            'r_state',
            'type',
            'type',
            'order'
        ]


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Order
        fields = [
            'id',
            'order_no',
            'date_create',
            'date_update',
            'products'
        ]


class ProductListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    document_name = serializers.CharField(read_only=True)
    file = serializers.URLField(read_only=True)


class TaskResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskResult
        fields = [
            'task_id',
            'task_name',
            'status',
            'result',
            'date_created',
            'date_done'
        ]
