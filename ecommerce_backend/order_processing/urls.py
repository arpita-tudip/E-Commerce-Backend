from django.urls import path
from . import views
from .views import MyProtectedView


urlpatterns = [
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    # path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),

    path('view-cart/', views.view_cart, name='view_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('protected/', MyProtectedView.as_view(), name='protected_view'),

]
