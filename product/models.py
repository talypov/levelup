import os

from django.db import models
from django.shortcuts import reverse


def document_path_and_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.document_name}.{ext}'

    return os.path.join('files/', filename)


class Order(models.Model):
    order_no = models.CharField(max_length=100, blank=False, null=False, db_index=True)
    date_create = models.DateTimeField(auto_now=True)
    date_update = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('order_detail_url', kwargs={'order_no': self.order_no})

    def __str__(self):
        return self.order_no


class Product(models.Model):
    TV = 'TV'
    MOBILE = 'MOBILE'
    AUDIO = 'AUDIO'
    PHOTO = 'PHOTO'

    TYPE_CHOICES = [(TV, 'TV set'),
                    (MOBILE, 'Mobile Phone'),
                    (AUDIO, 'Audio system'),
                    (PHOTO, 'Photo camera')]

    product_no = models.CharField(max_length=100, blank=False, null=False, db_index=True, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    r_state = models.CharField(max_length=100, blank=True, null=True)
    order = models.ManyToManyField(to=Order,
                                   related_name='products',
                                   verbose_name='Order')
    type = models.CharField(max_length=20, blank=True, null=True, choices=TYPE_CHOICES)
    qty = models.CharField(max_length=100, blank=False, null=False, default=1)

    def get_absolute_url(self):
        return reverse('product_detail_url', kwargs={'pk': self.id})

    def __str__(self):
        return self.product_no


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
