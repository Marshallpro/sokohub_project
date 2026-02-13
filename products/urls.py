from django.urls import path
from . import views




urlpatterns = [
    path('', views.home, name='home'),               # /products/
    path('list/', views.product_list, name='product_list'),
    path('dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('add/', views.add_product, name='add_product'),
    path('vendor/', views.vendor_products, name='vendor_products'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('<int:pk>/delete/', views.delete_product, name='delete_product'),
]