from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import vendor_required, customer_required
from .models import Product
from orders.models import OrderItem 
from django.db.models import Sum, Count, F
from .forms import ProductForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages 



@vendor_required 
def vendor_dashboard(request):
    vendor = request.user
    products = Product.objects.filter(vendor=vendor)
    total_products = products.count()
    active_products = products.filter(status='active').count()
    out_of_stock_products = products.filter(stock__lte=0).count() 
    

    pending_orders_count = OrderItem.objects.filter(
        product__vendor=vendor, 
        order__status='pending'
    ).values('order').distinct().count()

    recent_products = products.order_by('-created_at')[:5]
    
    context = {
        'total_products': total_products,
        'active_products': active_products,
        'out_of_stock_products': out_of_stock_products,
        'pending_orders_count': pending_orders_count,
        'recent_products': recent_products,
    }
    return render(request, 'products/vendor_dashboard.html', context)



@vendor_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user
            product.status = 'active' 
            product.save()
            messages.success(request, f"Product '{product.name}' created and listed successfully!")
            return redirect('vendor_products')
        
    else:
        form = ProductForm()
        
    context = {'form': form}
    return render(request, 'products/add_product.html', context)

@vendor_required
def vendor_products(request):
    vendor = request.user
    
    
    products = Product.objects.filter(vendor=vendor).order_by('-created_at')
    
    context = {
        'products': products
    }
    return render(request, 'products/vendor_products_list.html', context)

@login_required 
def product_list(request):
    products_list = Product.objects.filter(status='active')
    sort_by = request.GET.get('sort', '-created_at') 

    if sort_by == 'price_asc':
        products_list = products_list.order_by('price')
    elif sort_by == 'price_desc':
        products_list = products_list.order_by('-price')
    else:
        products_list = products_list.order_by('-created_at') 

    
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
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    # Fetch the product or return 404
    product = get_object_or_404(Product, pk=pk, status='active')
    
    
    max_quantity = min(product.stock, 10) 
    quantity_options = range(1, max_quantity + 1)
    
    context = {
        'product': product,
        'quantity_options': quantity_options,
    }
    return render(request, 'products/product_details.html', context)


def home(request):
    """Public home view."""
    return render(request, 'accounts/home.html', {'title': 'Home'})

@vendor_required
def edit_product(request, pk):  
    product = get_object_or_404(Product, pk=pk, vendor=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.name}' updated successfully!")
            return redirect('vendor_products')
    else:
        form = ProductForm(instance=product)
        
    context = {'form': form, 'product': product}
    return render(request, 'products/edit_product.html', context)

@vendor_required
def delete_product(request, pk):  
    product = get_object_or_404(Product, pk=pk, vendor=request.user)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, f"Product '{product.name}' deleted successfully!")
        return redirect('vendor_products')
    
    context = {'product': product}
    return render(request, 'products/delete_product.html', context)