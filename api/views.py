import logging
import time

from django_celery_results.models import TaskResult
from rest_framework import pagination
from rest_framework import viewsets
from rest_framework.decorators import parser_classes
from rest_framework.exceptions import UnsupportedMediaType
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_csv.parsers import CSVParser

from api.serializers import ProductSerializer, OrderSerializer, ProductListSerializer, \
    TaskResultSerializer
from product.models import Product, Order, ProductListCSV
from product.tasks import parse_csv_task

logger = logging.getLogger(__name__)


class PaginationClass(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductListApiView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    pagination_class = PaginationClass

    def get_queryset(self):
        return Product.objects.all()

    def get_object(self):
        product_id = self.kwargs.get('pk')
        if product_id:
            return self.get_queryset().filter(id=product_id).first()


class OrderListApiView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    pagination_class = PaginationClass

    def get_queryset(self):
        return Order.objects.all()

    def get_object(self):
        order_id = self.kwargs.get('pk')
        if order_id:
            return self.get_queryset().filter(id=order_id).first()


class TaskResultViewSet(viewsets.ModelViewSet):
    serializer_class = TaskResultSerializer
    pagination_class = PaginationClass

    def get_queryset(self):
        return TaskResult.objects.all()

    def get_object(self):
        task_id = self.kwargs.get('pk')
        if task_id:
            return self.get_queryset().filter(id=task_id).first()


class FileUploadView(GenericAPIView):
    serializer_class = ProductListSerializer

    @parser_classes([CSVParser])
    def post(self, request):
        file = request.FILES['file']
        if file.content_type == 'text/csv':
            filename = str(time.time())
        else:
            raise UnsupportedMediaType(file.content_type)

        upload_file = ProductListCSV.objects.create(document_name=filename, file=file)
        serializer = ProductListSerializer(upload_file, many=False)

        parse_csv_task.delay()

        return Response(serializer.data)
