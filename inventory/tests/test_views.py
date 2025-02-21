from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from inventory.models import Product, Order, OrderItem
from users.models import User

class ProductTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(email='admin@example.com', password='adminpass', role='admin')
        self.regular_user = User.objects.create_user(email='user@example.com', password='userpass', role='user')
        self.product_data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'quantity': 10,
            'price': 100.00
        }
        self.product = Product.objects.create(**self.product_data)

    def test_admin_can_create_product(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(reverse('product-list'), self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_regular_user_cannot_create_product(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(reverse('product-list'), self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_regular_user_can_view_products(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class OrderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass', role='user')
        self.admin_user = User.objects.create_user(email='admin@example.com', password='adminpass', role='admin')
        self.product = Product.objects.create(name='Test Product', description='Test Description', quantity=10, price=100.00)
        self.order = Order.objects.create(user=self.user, status='pending')
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2, price_at_order=100.00)

    def test_user_can_create_order(self):
        self.client.force_authenticate(user=self.user)
        order_data = {
            'items': [
                {
                    'product': self.product.id,
                    'quantity': 1,
                    'price_at_order': 100.00
                }
            ]
        }
        response = self.client.post(reverse('order-list'), order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_update_order_status(self):
        self.client.force_authenticate(user=self.admin_user)
        update_data = {'status': 'completed'}
        response = self.client.patch(reverse('update-order-status', args=[self.order.id]), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')

class ReportTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(email='admin@example.com', password='adminpass', role='admin')
        self.product_low_stock = Product.objects.create(name='Low Stock Product', description='Low Stock', quantity=5, price=50.00)
        self.product_high_stock = Product.objects.create(name='High Stock Product', description='High Stock', quantity=20, price=100.00)

    def test_low_stock_report(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('low-stock-report'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['products']), 1)
        self.assertEqual(response.data['products'][0]['name'], 'Low Stock Product')