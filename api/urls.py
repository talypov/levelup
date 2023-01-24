from django.conf.urls import url, include
from rest_framework import routers

from api import views
from api.views import FileUploadView

router = routers.DefaultRouter()
router.register(r'products', views.ProductListApiView, basename='api_products')
router.register(r'orders', views.OrderListApiView, basename='api_orders')
router.register(r'task-result', views.TaskResultViewSet, basename='api_tasks_result')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^upload/', FileUploadView.as_view(), name='products_uploader'),
]
