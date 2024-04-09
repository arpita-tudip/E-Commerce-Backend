
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

class ProductAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product1 = Product.objects.create(name='Test Product 1', description='Description 1', price=10.99, stock_quantity=100)
        self.product2 = Product.objects.create(name='Test Product 2', description='Description 2', price=20.99, stock_quantity=50)
        self.category = Category.objects.create(name='Test Category')

    def test_product_list(self):
        url = reverse('product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assuming two products are created in setUp

    def test_product_detail(self):
        url = reverse('product_detail', args=[self.product1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product 1')

    def test_product_create(self):
        url = reverse('product_create')
        data = {
            'name': 'New Product',
            'description': 'New Description',
            'price': 30.99,
            'stock_quantity': 200,
            'categories': [self.category.pk]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)  # Assuming there were 2 products before creating this one

class CategoryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category1 = Category.objects.create(name='Category 1')
        self.category2 = Category.objects.create(name='Category 2')

    def test_list_categories(self):
        url = reverse('list_categories')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assuming two categories are created in setUp


