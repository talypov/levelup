import logging
import os

from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import reverse

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

    def clean_product_no(self):
        product_number = self.product_no.strip()
        if not product_number.isalpha():
            raise ValidationError("Product number have to be string.")
        return product_number

    def clean_name(self):
        name = self.name.strip()
        if not name.isalpha():
            raise ValidationError("Name have to be string.")
        return name

    def clean_description(self):
        description = self.description.strip()
        if not description.isalpha():
            raise ValidationError("Description have to be string.")
        return description

    def clean_r_state(self):
        state = self.r_state.strip()
        if not state.isalpha():
            raise ValidationError("State have to be string.")
        return state

    def clean_type(self):
        type = self.type.strip()
        if not type.isalpha():
            raise ValidationError("Type have to be string.")
        return type

    def clean_qty(self):
        quantity = int(self.qty)
        if quantity < 0:
            raise ValidationError("Quantity must be greater 0.")
        return quantity

    @classmethod
    def from_csv(cls, row):
        product_no = row[0]
        name = row[1]
        description = row[2]
        r_state = row[3]
        type = row[5]
        qty = row[6]

        product = cls(product_no=product_no, name=name, description=description, r_state=r_state, type=type, qty=qty)
        try:
            product.clean_fields()
            product.clean()
            product.save()
            return product
        except Exception as e:
            logger.info(e)

    @staticmethod
    def is_new_product(row, csv_order_products) -> bool:
        product_no = row[0]
        order = row[4]
        product = Product.objects.filter(
            product_no=product_no,
            order__order_no=order
        ).first()
        return False if product and product.id in csv_order_products else True

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
