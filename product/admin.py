from django.contrib import admin

from .models import Product, Order


class ProductAdmin(admin.ModelAdmin):
    fields = ['product_no', 'name', 'description', 'r_state', 'type', 'order']
    list_display = ('product_no', 'name', 'r_state', 'type', 'get_order')

    def get_order(self, obj):
        return obj.order

    class Meta:
        model = Product


class OrderAdmin(admin.ModelAdmin):
    fields = ['order_no']   # поля в сингловой странице
    list_display = ('order_no', 'date_create', 'date_update')   # поля в таблице

    class Meta:
        model = Order


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
