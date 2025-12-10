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
    
]