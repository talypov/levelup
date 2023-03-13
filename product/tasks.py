import csv
import sys
from time import sleep
import logging
from celery import shared_task

from levelup.celery import app
from product.models import ProductListCSV, Order, Product

logger = logging.getLogger(__name__)

@shared_task
def bar():
    return 'Hello, world'


@app.task
def parse_csv_task():
    obj = ProductListCSV.objects.all().order_by('-date_create').first()

    if obj.is_done:
        logger.info('Import from last date CSV file already done')
    else:
        with open(obj.file.path, 'r') as csv_file:
            data = list(csv.reader(csv_file, delimiter=";"))
            rows = len(data)
            one_row_per = 100 / rows
            per_sum = one_row_per

            for row in data:
                csv_order = Order.objects.get_or_create(order_no=row[4])[0]
                csv_order_products = list(csv_order.products.all().values_list('id', flat=True))
                if len(csv_order_products) == 0 or Product.is_new_product(row, csv_order_products):
                    product = Product.from_csv(row)
                    csv_order.products.add(product)

                sys.stdout.write("[%-10s] %d%%" % ('=' * int(per_sum/10), per_sum))
                sleep(0.25)
                per_sum += one_row_per

        obj.is_done = True
        obj.save()
