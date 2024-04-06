from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def product_list(request):
    """
    List all products.
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    """
    Retrieve a single product by ID.
    """
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['POST'])
def product_create(request):
    """
    Create a new product.
    """
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def product_update(request, pk):
    """
    Update an existing product.
    """
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def product_delete(request, pk):
    """
    Delete an existing product.
    """
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return Response(status=204)
