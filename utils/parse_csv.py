from product.models import Product


def is_new_product(row, csv_order_products):
    product_no = row[0]
    r_state = row[3]
    order = row[4]
    product = Product.objects.filter(
        product_no=product_no,
        r_state=r_state,
        order__order_no=order
    ).first()
    if product and product.id in csv_order_products:
        return False
    else:
        return True
