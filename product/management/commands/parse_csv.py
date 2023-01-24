# import csv
# from django.core.management import BaseCommand
# from django.utils import timezone
#
# from product.models import ProductListCSV, Order, Product
#
#
# class Command(BaseCommand):
#     help = "Loads products and product categories from CSV file."
#
#     def handle(self, *args, **options):
#         start_time = timezone.now()
#         obj = ProductListCSV.objects.filter(is_done=False).order_by('-date_create').first()
#
#         with obj.file.open('r') as csv_file:
#             data = list(csv.reader(csv_file, delimiter=";"))
#
#             for row in data[1:]:
#                 csv_order = Order.objects.get_or_create(order_no=row[4])[0]
#                 csv_order_products = list(csv_order.products.all().values_list('id', flat=True))
#                 if len(csv_order_products) == 0 or is_new_product(row, csv_order_products):
#                     product = Product.objects.create(
#                         product_no=row[0],
#                         name=row[1],
#                         description=row[2],
#                         r_state=row[3],
#                         type=row[5],
#                         qty=row[6],
#                     )
#                     csv_order.products.add(product)
#             end_time = timezone.now()
#             self.stdout.write(
#                 self.style.SUCCESS(
#                     f"Loading CSV took: {(end_time - start_time).total_seconds()} seconds."
#                 )
#             )
#
#
# def is_new_product(row, csv_order_products):
#     product_no = row[0]
#     r_state = row[3]
#     order = row[4]
#     product = Product.objects.filter(product_no=product_no,
#     r_state=r_state, order__order_no=order).first()
#     if product and product.id in csv_order_products:
#         return False
#     else:
#         return True

# рабочий

# def import_product_csv():
#     start_time = timezone.now()
#     obj = ProductListCSV.objects.filter(is_done=False).order_by('-date_create').first()
#
#     with obj.file.open('r') as csv_file:
#         data = list(csv.reader(csv_file, delimiter=";"))
#         for row in data[1:]:
#             csv_order = Order.objects.get_or_create(order_no=row[4])[0]
#             csv_order_products = list(csv_order.products.all().values_list('id', flat=True))
#             if len(csv_order_products) == 0 or is_new_product(row, csv_order_products):
#                 product = Product.objects.create(
#                     product_no=row[0],
#                     name=row[1],
#                     description=row[2],
#                     r_state=row[3],
#                     type=row[5],
#                     qty=row[6],
#                 )
#                 csv_order.products.add(product)
#
#     end_time = timezone.now()
