from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order, OrderItem, Cart, CartItem
from .serializers import OrderSerializer, CartSerializer
from product_management.models import Product  # Import Product model from product_management app

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi




class MyProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user  # Access the authenticated user
        user_details = {
            'username': user.username,
            'email': user.email,
            # Add other user details as needed
        }
        content = {
            'message': 'This is a protected endpoint!',
            'user': user_details,
        }
        return Response(content)






schema = {
    "product_id": openapi.Schema(type=openapi.TYPE_INTEGER),
    "quantity": openapi.Schema(type=openapi.TYPE_INTEGER)
}

@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties=schema,
    required=['product_id']
))
@api_view(['POST'])
def add_to_cart(request):
    """
    Add a product to the user's cart.
    """
    data = request.data
    user = request.user.id

    print("data>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", data)
    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user)

    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1)) 

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    # Retrieve or create the cart item
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, quantity=quantity)

    # Update the quantity
    cart_item.quantity += quantity
    cart_item.save()

    # Serialize the cart and return response
    serializer = CartSerializer(cart)
    return Response(serializer.data)

# @swagger_auto_schema(method='get', operation_description="View the user's shopping cart")
@api_view(['GET'])
def view_cart(request):
    """
    View the user's shopping cart.
    """
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    except Cart.DoesNotExist:
        return Response({'message': 'Cart is empty'}, status=404)


    
@swagger_auto_schema(method='post', operation_description="Place an order using the items in the user's cart")
@api_view(['POST'])
def place_order(request):
    """
    Place an order using the items in the user's cart.
    """
    user = request.user

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    if cart.items.count() == 0:
        return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

    # Calculate total amount
    total_amount = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())

    # Create order
    order = Order.objects.create(user=user, total_amount=total_amount)

    # Create order items and update stock quantities
    for cart_item in cart.cartitem_set.all():
        product = cart_item.product
        quantity = cart_item.quantity
        OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
        product.stock_quantity -= quantity
        product.save()

    # Clear the user's cart
    cart.cartitem_set.all().delete()

    return Response({"message": "Order placed successfully"}, status=status.HTTP_201_CREATED)





@swagger_auto_schema(method='put', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties=schema,
    required=['product_id']
))
@api_view(['PUT'])
def update_cart(request):
    """
    Update quantity of a product in the user's cart.
    """
    data = request.data
    user = request.user

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))

    try:
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.quantity = quantity
        cart_item.save()
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CartSerializer(cart)
    return Response(serializer.data)

@swagger_auto_schema(method='delete', operation_description="Remove a product from the user's cart")
@api_view(['DELETE'])
def delete_cart(request):
    """
    Remove a product from the user's cart.
    """
    data = request.data
    user = request.user

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    product_id = data.get('product_id')

    try:
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.delete()
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CartSerializer(cart)
    return Response(serializer.data)