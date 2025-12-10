from django.urls import path
from . import views

urlpatterns = [
    path('my-orders/', views.customer_order_history, name='customer_orders'), 
    path('checkout/<int:product_id>/', views.simple_checkout, name='simple_checkout'),
    path('order/confirm/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('vendor/orders/', views.vendor_order_management, name='vendor_orders'),
]