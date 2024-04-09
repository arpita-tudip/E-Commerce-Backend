from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(method='get', operation_description="List all products")
@api_view(['GET'])
def product_list(request):
    """
    List all products.
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@swagger_auto_schema(method='get', operation_description="Retrieve a single product by ID")
@api_view(['GET'])
def product_detail(request, pk):
    """
    Retrieve a single product by ID.
    """
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)



product_create_schema = {
    "name": openapi.Schema(type=openapi.TYPE_STRING, description="Product name"),
    "description": openapi.Schema(type=openapi.TYPE_STRING, description="Product description"),
    "price": openapi.Schema(type=openapi.TYPE_NUMBER, description="Product price"),
    "stock_quantity": openapi.Schema(type=openapi.TYPE_INTEGER, description="Stock quantity"),
    "categories": openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Items(type=openapi.TYPE_STRING),
        description="List of categories the product belongs to"
    )
}
@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties=product_create_schema,
    required=["name", "description", "price", "stock_quantity", "categories"]
))
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

@swagger_auto_schema(method='put', operation_description="Update an existing product")
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

@swagger_auto_schema(method='delete', operation_description="Delete an existing product")
@api_view(['DELETE'])
def product_delete(request, pk):
    """
    Delete an existing product.
    """
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return Response(status=204)
