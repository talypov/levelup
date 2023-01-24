from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from product.forms import ProductForm, OrderForm
from product.models import Product, Order


class ProductList(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'product/index.html', context={'products': products})


class ProductDetail(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    slug_field = 'product_no'       # this is the model field name.
    slug_url_kwarg = 'product_no'  # this the `argument` in the URL conf

# Обязательные строчки, указывающие по каким параметрам выбирать объект в БД


class ProductUpdate(UpdateView):
    model = Product
    fields = ('name', 'description', 'r_state', 'order', 'type')
    template_name = 'product/update_product.html'
    success_url = reverse_lazy('product_list_url')

    # Если объект вызывается не через ID то надо переписать get_object
    # чтобы возвращало твой объект по product_no
    # def get_object(self, queryset=None):
    #     if queryset is None:
    #         queryset = self.get_queryset()
    #     product_no = self.kwargs.get('id')
    #
    #     queryset = queryset.filter(product_no=product_no)
    #     obj = queryset.get()
    #     return obj


class ProductCreate(CreateView):
    form_class = ProductForm
    template_name = 'product/add_product.html'
    success_url = reverse_lazy('product_list_url')


class OrderCreate(CreateView):
    form_class = OrderForm
    template_name = 'product/add_order.html'
    success_url = reverse_lazy('product_list_url')


class OrderList(View):
    def get(self, request):
        orders = Order.objects.all()
        return render(request, 'product/orders.html', context={'orders': orders})


class OrderDetail(View):
    def get(self, request, order_no):
        order = get_object_or_404(Order, order_no__iexact=order_no)
        products = Product.objects.filter(order=order.id)
        context = {
            'order': order,
            'products': products,
        }
        return render(request, 'product/order_detail.html', context=context)


class OrderUpdate(UpdateView):
    model = Order
    fields = ('order_no',)
    template_name = 'product/update_order.html'
    success_url = reverse_lazy('order_list_url')

    # Если объект вызывается не через ID то надо переписать get_object
    # чтобы возвращало твой объект по product_no
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        order_no = self.kwargs.get('order_no')

        queryset = queryset.filter(order_no=order_no)
        obj = queryset.get()
        return obj


class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('product_list_url')
    template_name = 'product/delete_product.html'

    # def get_object(self, queryset=None):
    #     if queryset is None:
    #         queryset = self.get_queryset()
    #     product_no = self.kwargs.get('product_no')
    #
    #     queryset = queryset.filter(product_no=product_no)
    #     obj = queryset.get()
    #     return obj


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('order_list_url')
    template_name = 'product/delete_order.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        order_no = self.kwargs.get('order_no')

        queryset = queryset.filter(order_no=order_no)
        obj = queryset.get()
        return obj
