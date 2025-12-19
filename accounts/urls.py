from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView  
from .maxins import CustomLoginRedirectMixin

 
urlpatterns = [
    
    path('', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', CustomLoginView.as_view(
        template_name='accounts/login.html'
    ), name='login'),

    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('two_factor/', views.two_factor_view, name='two_factor'),    
]