
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Order, OrderItem, Cart, CartItem
from product_management.models import Product

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(name='Test Product', description='Test description', price=10, stock_quantity=100)
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_add_to_cart(self):
        url = reverse('add_to_cart')
        data = {'product_id': self.product.id, 'quantity': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_cart(self):
        url = reverse('view_cart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_place_order(self):
        url = reverse('place_order')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_protected_view(self):
        url = reverse('protected_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_cart(self):
        url = reverse('update_cart')
        data = {'product_id': self.product.id, 'quantity': 3}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_cart(self):
        url = reverse('delete_cart')
        data = {'product_id': self.product.id}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


