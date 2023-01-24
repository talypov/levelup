import time

from django.http import HttpResponse
from django_celery_results.models import TaskResult
from rest_framework import viewsets, status
from rest_framework.decorators import parser_classes, action
from rest_framework.exceptions import UnsupportedMediaType
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_csv.parsers import CSVParser
from rest_framework.request import Request

from api.serializers import ProductSerializer, OrderSerializer, ProductListSerializer,\
    TaskResultSerializer
from product.models import Product, Order, ProductListCSV
from product.tasks import parse_csv_task


# class ProductListApiView(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

class ProductListApiView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        p_id = self.kwargs['pk']
        return self.get_queryset().filter(id=p_id).first()

    # def retrieve(self, request, *args, **kwargs):
    #     try:
    #         instance = self.get_object()
    #     except (Product.DoesNotExist, KeyError):
    #         return Response(
    #             {"error": "Requested Product does not exist"}, status=status.HTTP_404_NOT_FOUND
    #         )
    #     serializer = self.get_serializer(instance)
    #
    #     return Response(serializer.data)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

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

#
# class OrderListApiView(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer


class OrderListApiView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        o_id = self.kwargs['pk']
        return self.get_queryset().filter(id=o_id).first()

    # def retrieve(self, request, *args, **kwargs):
    #     try:
    #         instance = self.get_object()
    #     except (Order.DoesNotExist, KeyError):
    #         return Response(
    #             {"error": "Requested Order does not exist"}, status=status.HTTP_404_NOT_FOUND
    #         )
    #     serializer = self.get_serializer(instance)
    #
    #     return Response(serializer.data)
    #
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #
    # def perform_create(self, serializer):
    #     serializer.save()


class TaskResultViewSet(viewsets.ModelViewSet):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        t_id = self.kwargs['pk']
        return self.get_queryset().filter(id=t_id).first()

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except (TaskResult.DoesNotExist, KeyError):
            return Response(
                {"error": "Requested TaskResult does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
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
            filename = time.time()
        else:
            raise UnsupportedMediaType(file.content_type)

        doc = ProductListCSV.objects.create(document_name=filename, file=file)
        serializer = ProductListSerializer(doc, many=False)

        parse_csv_task.delay()

        return Response(serializer.data)


# class TaskstatusView(APIView):
#     # serializer_class = ProductListSerializer
#     # queryset = TaskResult.objects.all()
#     http_method_names = ['get', 'head']
#
#     def get_queryset(self):
#         return TaskResult.objects.filter(task_id=self.kwargs["task_id"]).first()

    # def get(self, request, format=None):
    #     users = TaskResult.objects.all()
    #     serializer = ProductListSerializer(users)
    #     return Response(serializer.data)

    # def get(self, request, *args, **kwargs):
    #     task_id = kwargs.get('task_id')
    #     result = TaskResult.objects.get(task_id=task_id)
    #     # results = TaskResult.objects.all()
    #     serializer = ProductListSerializer(result)
    #     return Response(serializer.data)

    # # def get(self, *args, **kwargs):
    # def get(self, *args, **kwargs):
    #     task_id = kwargs.get('task_id')
    #     result = TaskResult.objects.get(task_id=task_id)
    #
    #     return Response(result.status)

# class TaskstatusView(APIView):
#     """
#     Create a new user. It's called 'UserList' because normally we'd have a get
#     method here too, for retrieving a list of all User objects.
#     """
#     http_method_names = ['get', 'head']
#
#     def get(self, request, *args, **kwargs):
#         task_id = kwargs.get('task_id')
#         serializer = TaskResultSerializer(TaskResult.objects.get(task_id=task_id), many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
