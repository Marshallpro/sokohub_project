from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from functools import wraps

def role_required(allowed_roles=None):
    """
    Decorator to check if the user is logged in and has one of the allowed roles.
    """
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            user = request.user
            
           
            if not user.is_authenticated:
                messages.warning(request, "Please log in to view this page.")
                return redirect(f"{reverse('login')}?next={request.path}")

           
            if user.user_type in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                
                messages.error(request, "You are not authorized to access this page.")
                
                
                if user.user_type == 'vendor':
                    return redirect('vendor_dashboard')
                elif user.user_type == 'customer':
                    return redirect('product_list')
                
                
                return redirect('home') 

        return wrapper_func
    return decorator


def vendor_required(view_func):
    return role_required(allowed_roles=['vendor'])(view_func)

def customer_required(view_func):
    return role_required(allowed_roles=['customer'])(view_func)