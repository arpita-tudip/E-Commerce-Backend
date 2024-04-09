from django.urls import path
from . import views
from .views import MyProtectedView


urlpatterns = [
    path('cart/add', views.add_to_cart, name='add_to_cart'),
    path('cart/view', views.view_cart, name='view_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('protected/', MyProtectedView.as_view(), name='protected_view'),

    path('cart/update', views.update_cart, name='update_cart'),
    path('cart/delete', views.delete_cart, name='delete_cart'),

]
