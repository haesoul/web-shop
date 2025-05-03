
from django.urls import path

from cart_order.views import *

app_name = 'cart_order'



urlpatterns = [
    path('cart-items/',CartItemView.as_view(),name='cart_items_view'),
    path('add-order/<slug:slug>/',AddOrderView.as_view(),name='add_order'),
    path('orders/',OrderListView.as_view(),name='order_list'),
    path('order/<slug:slug>/',OrderDetailView.as_view(),name='order_detail'),

]
