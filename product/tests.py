import json

from django.contrib.auth.models import User
from django_celery_results.models import TaskResult

from levelup.tests import LevelUpAPITestCase
from product.models import Order, Product, ProductListCSV
from product.tasks import parse_csv_task


class TestCsulReleaseViewSet(LevelUpAPITestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.get(username='test')
        self.client.login(username=self.user.username, password='test')
        self.order = Order.objects.create(order_no='order_001')
        self.order2 = Order.objects.create(order_no='order_002')
        self.product1 = Product.objects.create(
            product_no="test-1",
            name="test_product-1",
            r_state="A2",
            type="TV",
        )
        self.product2 = Product.objects.create(
            product_no="test-2",
            name="test_product-2",
            r_state="A2",
            type="MOBILE",
        )
        self.order.products.add(self.product1)
        self.order.products.add(self.product2)

    def test_product_create_success(self):
        data = json.dumps({
            "product_no": "test-3",
            "name": "test_product",
            "r_state": "A2",
            "type": "TV",
            "order": [
                self.order.id
            ]
        })

        response = self.client.post('/api/products/', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['product_no'], 'test-3')

    def test_product_update_success(self):
        data = json.dumps({
            "product_no": "put_test-3",
            "name": "put_test_product",
            "order": [
                self.order.id
            ]
        })

        response = self.client.put(
            '/api/products/{}/'.format(self.product1.id),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['product_no'], 'put_test-3')
        product = Product.objects.filter(id=self.product1.id).first()
        self.assertEqual(product.product_no, 'put_test-3')
        self.assertEqual(product.name, 'put_test_product')
        self.assertEqual(product.r_state, 'A2')

    def test_get_product_by_id_success(self):
        response = self.client.get('/api/products/{}/'.format(self.product1.id), format='json')
        data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], self.product1.id)
        self.assertEqual(data['product_no'], self.product1.product_no)
        self.assertEqual(data['name'], self.product1.name)
        self.assertEqual(data['r_state'], self.product1.r_state)
        self.assertEqual(data['type'], self.product1.type)

    def test_delete_product_by_id_success(self):
        response = self.client.delete('/api/products/{}/'.format(self.product1.id), format='json')

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Product.objects.filter(id=self.product1.id).exists())

    def test_products_list_success(self):
        response = self.client.get('/api/products/', format='json')
        products_db = Product.objects.all().count()
        products_rq = response.data.get('count')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(products_db, products_rq)

    def test_order_create_success(self):
        data = json.dumps({
            "order_no": "order_003",
        })

        response = self.client.post('/api/orders/', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['order_no'], 'order_003')

    def test_order_update_success(self):
        data = json.dumps({
            "order_no": "order_002",
        })

        response = self.client.put(
            '/api/orders/{}/'.format(self.order.id),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['order_no'], 'order_002')
        order = Order.objects.filter(id=self.order.id).first()
        self.assertEqual(order.order_no, 'order_002')

    def test_get_order_by_id_success(self):
        response = self.client.get('/api/orders/{}/'.format(self.order.id), format='json')
        data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], self.order.id)
        self.assertEqual(data['order_no'], self.order.order_no)

    def test_order_list_success(self):
        response = self.client.get('/api/orders/', format='json')
        products_db = Order.objects.all().count()
        products_rq = response.data.get('count')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(products_db, products_rq)

    def test_delete_order_by_id_success(self):
        response = self.client.delete('/api/orders/{}/'.format(self.order.id), format='json')

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())


class TestParseCSV(LevelUpAPITestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.get(username='test')
        self.client.login(username=self.user.username, password='test')

    def test_parse_csv_success(self):
        ProductListCSV.objects.create(document_name='test-csv', file='files/test-csv.csv')
        TaskResult.objects.create(task_id='test_task')
        parse_csv_task()
        products = Product.objects.all()
        orders = Order.objects.all()

        product1 = products.get(product_no='111')
        prod_to_ord1 = orders.get(order_no='order111').products.all()
        prod_to_ord2 = orders.get(order_no='order222').products.all()
        productlist = ProductListCSV.objects.get(document_name='test-csv')

        self.assertEqual(products.count(), 3)
        self.assertEqual(orders.count(), 2)
        self.assertEqual(prod_to_ord1.count(), 2)
        self.assertEqual(prod_to_ord2.count(), 1)
        self.assertEqual(product1.name, 'product111')
        self.assertEqual(product1.description, 'description 111')
        self.assertEqual(product1.type, 'MOBILE')
        self.assertEqual(productlist.is_done, True)
