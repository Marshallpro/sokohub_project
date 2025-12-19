from django.urls import path
from . import views

urlpatterns = [
    path('momo/<int:order_id>/', views.momo_payment, name='momo_payment'),
    path('status/<int:payment_id>/', views.payment_status, name='payment_status'),
]
