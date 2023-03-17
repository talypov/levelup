import logging
import os

from django.db import models
from django.shortcuts import reverse

from api.utils.product_data import ProductData

logger = logging.getLogger(__name__)

def document_path_and_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.document_name}.{ext}'

    return os.path.join('media', filename)


class Order(models.Model):
    order_no = models.CharField(max_length=100, blank=False, null=False, db_index=True)
    date_create = models.DateTimeField(auto_now=True)
    date_update = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('order_detail_url', kwargs={'order_no': self.order_no})

    def __str__(self):
        return self.order_no


class ProductModelManager(models.Manager):
    def create_from_productdata(self, productdata: ProductData):
        try:
            product_model = self.model(
                product_no=productdata.product_no,
                name=productdata.name,
                description=productdata.description,
                r_state=productdata.r_state,
                type=productdata.type,
                qty=productdata.qty
            )
            product_model.save()
            return product_model
        except Exception as e:
            logger.info(e)



class Product(models.Model):
    TV = 'TV'
    MOBILE = 'MOBILE'
    AUDIO = 'AUDIO'
    PHOTO = 'PHOTO'

    TYPE_CHOICES = [(TV, 'TV set'),
                    (MOBILE, 'Mobile Phone'),
                    (AUDIO, 'Audio system'),
                    (PHOTO, 'Photo camera')]

    product_no = models.CharField(max_length=100, blank=False, null=False, db_index=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    r_state = models.CharField(max_length=100, blank=True, null=True)
    order = models.ManyToManyField(to=Order,
                                   related_name='products',
                                   verbose_name='Order')
    type = models.CharField(max_length=20, blank=True, null=True, choices=TYPE_CHOICES)
    qty = models.CharField(max_length=100, blank=False, null=False, default=1)

    @staticmethod
    def is_new_product(row, csv_order_products) -> bool:
        product_no = row.get('product_no', None)
        order = row.get('order', None)
        product = Product.objects.filter(
            product_no=product_no,
            order__order_no=order
        ).first()
        return False if product and product.id in csv_order_products else True

    def get_absolute_url(self):
        return reverse('product_detail_url', kwargs={'pk': self.id})

    def __str__(self):
        return self.product_no

    objects = ProductModelManager()


class ProductListCSV(models.Model):
    # I'm using document_name and id to give the filename that would be save with
    # this using document_path_and_name function.
    # you can modify on your need.
    document_name = models.CharField(max_length=100)
    date_create = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to=document_path_and_name)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.document_name
