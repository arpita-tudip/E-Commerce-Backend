from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order, OrderItem, Cart, CartItem
from .serializers import OrderSerializer, CartSerializer
from product_management.models import Product  # Import Product model from product_management app

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

# class MyProtectedView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):
#         content = {
#             'message': 'This is a protected endpoint!',
#             'user': str(request.user),  # Access the authenticated user
#         }
#         return Response(content)

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

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



@api_view(['POST'])
def add_to_cart(request):
    """
    Add a product to the user's cart.
    """
    data = request.data
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user)
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
    serializer = CartSerializer(cart)
    return Response(serializer.data)

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

@api_view(['POST'])
def place_order(request):
    """
    Place an order using the items in the user's cart.
    """
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
        order = Order.objects.create(user=user, total_amount=cart.total_amount)
        for cart_item in cart.cart_items.all():
            OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity, price=cart_item.product.price)
        cart.delete()
        return Response({'message': 'Order placed successfully'})
    except Cart.DoesNotExist:
        return Response({'message': 'Cart is empty'}, status=400)
