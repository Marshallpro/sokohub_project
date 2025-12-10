from django.shortcuts import redirect
from django.contrib.auth.views import LoginView  
from django.urls import reverse_lazy 

class CustomLoginRedirectMixin:
   
    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.user_type == 'vendor':
                return reverse_lazy('vendor_dashboard')
            else:
                return reverse_lazy('product_list')
        return reverse_lazy('home') 

class CustomLoginView(CustomLoginRedirectMixin, LoginView):
    """
    This class correctly combines the mixin logic with 
    Django's base LoginView, giving it the .as_view() method.
    """
    pass