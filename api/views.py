import time

from django.shortcuts import get_object_or_404
from django_celery_results.models import TaskResult
from rest_framework import viewsets, status
from rest_framework.decorators import parser_classes
from rest_framework.exceptions import UnsupportedMediaType
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_csv.parsers import CSVParser

from api.serializers import ProductSerializer, OrderSerializer, ProductListSerializer, \
    TaskResultSerializer
from product.models import Product, Order, ProductListCSV
from product.tasks import parse_csv_task


class ProductListApiView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()

    def get_object(self):
        p_id = self.kwargs.get('pk')
        if p_id:
            return self.get_queryset().filter(id=p_id).first()

    # def destroy(self, request, *args, **kwargs):
    #     try:
    #         instance = self.get_object()
    #         self.perform_destroy(instance)
    #     except Exception:
    #         pass
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    # def destroy(self, request, *args, **kwargs):
    #     p_id = self.kwargs['pk']
    #     self.get_queryset().filter(id=p_id).first().delete()
    #     return super().destroy(request, *args, **kwargs)

    # def destroy(self, request, *args, **kwargs):
    #     p_id = self.kwargs['pk']
    #     product = self.get_queryset().filter(id=p_id).first().delete()
    #     # product = self.get_queryset().filter(id=p_id).first()
    #     return HttpResponse(status=status.HTTP_200_OK)

    # def create(self, request, *args, **kwargs):
    #     response = super().create(request, *args, **kwargs)
    #     instance = response.data
    #     return Response({'status': 'success'})

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #
    # def perform_create(self, serializer):
    #     serializer.save()


class OrderListApiView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.all()

    def get_object(self):
        o_id = self.kwargs.get('pk')
        if o_id:
            return self.get_queryset().filter(id=o_id).first()


class TaskResultViewSet(viewsets.ModelViewSet):
    serializer_class = TaskResultSerializer

    def get_queryset(self):
        return TaskResult.objects.all()

    def get_object(self):
        t_id = self.kwargs.get('pk')
        if t_id:
            return self.get_queryset().filter(id=t_id).first()

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), **kwargs)
        serializer = self.get_serializer(instance)
        if serializer.data["status"]:
            return Response(f'Task status - {serializer.data["status"]}')
        else:
            return Response("Requested Task does not exist")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
