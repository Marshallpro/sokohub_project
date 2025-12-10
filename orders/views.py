from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from products.models import Product
from .models import Order, OrderItem
from .forms import CheckoutForm
from accounts.decorators import customer_required, vendor_required
from django.db.models import F

@customer_required 
@transaction.atomic
def simple_checkout(request, product_id):
    product = get_object_or_404(Product, id=product_id, status='active')
    
   
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        
        try:
            quantity = int(request.POST.get('quantity'))
        except (ValueError, TypeError):
            quantity = 0

        if quantity <= 0 or quantity > product.stock:
            messages.error(request, "Invalid quantity requested or item is out of stock.")
            return redirect('product_details', pk=product.id)
            
        if form.is_valid():
            unit_price = product.price
            order_total = unit_price * quantity
            
           
            order = Order.objects.create(
                customer=request.user,
                total=order_total,
                status='pending',
                delivery_address=form.cleaned_data['delivery_address'],
                phone=form.cleaned_data['phone']
            )
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=unit_price 
            )
            
            product.stock -= quantity
            product.save()
            messages.success(request, f"Order #{order.id} placed successfully!")
            return redirect('order_confirmation', order_id=order.id)

    else: 
        initial_data = {
            'phone': request.user.phone,
            'delivery_address': request.user.location,
        }
        form = CheckoutForm(initial=initial_data)
    
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1
        
    context = {
        'product': product,
        'quantity': quantity,
        'unit_price': product.price,
        'total': product.price * quantity,
        'form': form,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    order_item = order.items.first() 

    context = {
        'order': order,
        'item': order_item,
    }
    return render(request, 'orders/order_confirmation.html', context)

@customer_required 
def customer_order_history(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'orders/customer_orders.html', context)

@vendor_required 
def vendor_order_management(request):
    vendor = request.user
    
    vendor_order_items = OrderItem.objects.filter(product__vendor=vendor).order_by('-order__created_at')
    
    context = {
        'order_items': vendor_order_items,
    }
    return render(request, 'orders/vendor_orders.html', context)