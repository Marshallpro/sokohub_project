from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .decorators import vendor_required, customer_required
from .form import RegistrationForm
from .decorators import vendor_required, customer_required 

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST) 
        if form.is_valid():
            user = form.save()
            login(request, user) 
            if user.user_type == 'vendor':
                return redirect('vendor_dashboard') 
            else:
                return redirect('product_list') 
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

class CustomLoginView(LoginView):
    """
    Custom Login View that redirects users based on their user_type 
    (vendor or customer) upon successful login.
    """
    def get_success_url(self):
        url = self.get_redirect_url()
        if url:
            # Handles the 'next' parameter redirection
            return url
            
        # Custom redirect logic based on user_type
        if self.request.user.is_authenticated:
            if self.request.user.user_type == 'vendor':
                return reverse('vendor_dashboard')
            else:
                return reverse('product_list')
        
        # Fallback if somehow not authenticated
        return super().get_success_url()



def home(request):
    """Public home view."""
    return render(request, 'accounts/home.html', {'title': 'Home'})

@vendor_required 
def vendor_dashboard(request):
    """View protected for vendors only."""
    return render(request, 'accounts/vendor_dashboard.html', {'title': 'Vendor Dashboard'})


@customer_required 
def customer_orders(request):
    """View protected for customers only."""
    return render(request, 'accounts/customer_orders.html', {'title': 'My Orders'})

def placeholder_product_list(request):
    """Placeholder for the main product listing page."""
    return render(request, 'products/product_list.html', {'title': 'All Products'})