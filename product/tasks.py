import csv
import sys
from time import sleep

from celery import shared_task
from django_celery_results.models import TaskResult

from levelup.celery import app
from product.models import ProductListCSV, Order, Product
from utils.parse_csv import is_new_product


@shared_task
def bar():
    return 'Hello, world'

# @app.task
# def parse_csv_task():
#     # obj = ProductListCSV.objects.filter(is_done=False).order_by('-date_create').first()
#     obj = ProductListCSV.objects.all().order_by('-date_create').first()
#
#     if obj.is_done:
#         raise Exception('Import from last date CSV file already done')
#     else:
#         with obj.file.open('r') as csv_file:
#             data = list(csv.reader(csv_file, delimiter=";"))
#             for i in range(len(data[1:])):
#                 # sys.stdout.write('\r')
#                 sys.stdout.write("[%-20s] %d%%" % ('=' * i, 5 * i))
#                 # sys.stdout.flush()
#                 sleep(0.25)
#                 for row in data[1:]:
#                     csv_order = Order.objects.get_or_create(order_no=row[4])[0]
#                     csv_order_products = list(csv_order.products.all().values_list(
#                     'id', flat=True)
#                     )
#                     if len(csv_order_products) == 0 or is_new_product(row, csv_order_products):
#                         product = Product.objects.create(
#                             product_no=row[0],
#                             name=row[1],
#                             description=row[2],
#                             r_state=row[3],
#                             type=row[5],
#                             qty=row[6],
#                         )
#                         csv_order.products.add(product)
#
#         print(f'Operation id-{TaskResult.objects.last().task_id}')
#         obj.is_done = True
#         obj.save()
#         print('Parse completed')


@app.task
def parse_csv_task():
    obj = ProductListCSV.objects.all().order_by('-date_create').first()

    if obj.is_done:
        raise Exception('Import from last date CSV file already done')
    else:
        with obj.file.open('r') as csv_file:
            data = list(csv.reader(csv_file, delimiter=";"))
            rows = len(data[1:])
            one_row_per = 100 / rows
            five = 5
            per_sum = one_row_per

            for row in data[1:]:
                csv_order = Order.objects.get_or_create(order_no=row[4])[0]
                csv_order_products = list(csv_order.products.all().values_list('id', flat=True))
                if len(csv_order_products) == 0 or is_new_product(row, csv_order_products):
                    product = Product.objects.create(
                        product_no=row[0],
                        name=row[1],
                        description=row[2],
                        r_state=row[3],
                        type=row[5],
                        qty=row[6],
                    )
                    csv_order.products.add(product)

                if per_sum >= five:
                    sys.stdout.write("[%-20s] %d%%" % ('=' * int(five / 5), per_sum))
                    sleep(0.25)
                    five += 5
                per_sum += one_row_per

        print(f'Operation id-{TaskResult.objects.last().task_id}')
        obj.is_done = True
        obj.save()
        print('Parse completed')
