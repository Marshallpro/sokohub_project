from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('vendor/products/add/', views.add_product, name='add_product'),
    path('vendor/products/', views.vendor_products, name='vendor_products'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),
]