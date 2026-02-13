from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.auth.views import LoginView
from .decorators import vendor_required, customer_required
from .form import RegistrationForm, TwoFactorForm
from .decorators import vendor_required, customer_required 
from products.models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import reverse_lazy
from .models import User
import random
from django.contrib import messages 




class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'




def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST) 
        if form.is_valid():
            user = form.save()
            login(request, user) 
            if user.user_type == 'vendor':
                return redirect('vendor_dashboard') 
            else:
                return redirect('home') 
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

otp_storage = {}

class CustomLoginView(LoginView):
    """
    Custom Login View that optionally supports OTP,
    and redirects users based on user_type after login.
    """
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        """
        Log in user and redirect based on role.
        Optional: generate OTP if email backend is configured.
        """
        user = form.get_user()

        # Optional OTP generation (safe if email backend not configured)
        try:
            otp = f"{random.randint(100000, 999999)}"
            otp_storage[user.username] = otp
            # Try sending email, but fail silently if not configured
            user.email_user(
                subject="Your Soko Hub Login OTP",
                message=f"Your login verification code is: {otp}",
            )
            self.request.session['pre_2fa_user'] = user.username
            # Redirect to 2FA page
            return redirect('two_factor')
        except Exception:
            # If email fails, log in immediately
            from django.contrib.auth import login
            login(self.request, user)
            return self.get_success_url()

    def get_success_url(self):
        """
        Redirect users after login based on their role.
        """
        if self.request.user.is_authenticated:
            if self.request.user.user_type == 'vendor':
                return reverse('vendor_dashboard')
            elif self.request.user.user_type == 'customer':
                return reverse('product_list')
            else:
                return reverse('home')
        return super().get_success_url()


def two_factor_view(request):
    """
    OTP verification page. Optional if OTP/email not used.
    """
    username = request.session.get('pre_2fa_user')
    if not username:
        return redirect('login')

    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if otp_storage.get(username) == code:
                user = User.objects.get(username=username)
                from django.contrib.auth import login
                login(request, user)
                otp_storage.pop(username, None)
                messages.success(request, "Login successful!")

                # Redirect based on role
                if user.user_type == 'vendor':
                    return redirect('vendor_dashboard')
                elif user.user_type == 'customer':
                    return redirect('product_list')
                else:
                    return redirect('home')
            else:
                messages.error(request, "Invalid verification code.")
    else:
        form = TwoFactorForm()

    return render(request, 'accounts/two_factor.html', {'form': form})

def home(request):
    # Fetch all active products
    products_list = Product.objects.filter(status='active')
    
    # Handle sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by == 'price_asc':
        products_list = products_list.order_by('price')
    elif sort_by == 'price_desc':
        products_list = products_list.order_by('-price')
    else:
        products_list = products_list.order_by('-created_at')

    # Pagination
    paginator = Paginator(products_list, 12)
    page_number = request.GET.get('page')
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'current_sort': sort_by,
        'title': 'Home',
    }

    return render(request, 'products/product_list.html', context)

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