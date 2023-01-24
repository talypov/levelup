from django.urls import path

from product.views import ProductList, ProductDetail, OrderDetail, OrderList,\
    ProductDelete, OrderDelete, ProductUpdate, ProductCreate, OrderCreate, OrderUpdate

urlpatterns = [
    path('', ProductList.as_view(), name='product_list_url'),
    path('add/', ProductCreate.as_view(), name='product_add_url'),
    path('product/<int:pk>/', ProductDetail.as_view(), name='product_detail_url'),
    path('product/<int:pk>/update/', ProductUpdate.as_view(), name='product_update_url'),
    path('product/<int:pk>/delete/', ProductDelete.as_view(), name='product_delete_url'),
    path('add-order/', OrderCreate.as_view(), name='order_add_url'),
    path('orders/', OrderList.as_view(), name='order_list_url'),
    path('order/<str:order_no>/', OrderDetail.as_view(), name='order_detail_url'),
    path('order/<str:order_no>/update/', OrderUpdate.as_view(), name='order_update_url'),
    path('order/<str:order_no>/delete/', OrderDelete.as_view(), name='order_delete_url'),
]
