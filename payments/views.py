# payments/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order
from .models import Payment

@login_required
def momo_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    if request.method == "POST":
        phone = request.POST.get('phone')

        payment = Payment.objects.create(
            customer=request.user,
            order=order,
            amount=order.total,
            phone_number=phone,
            
        )

        # 🔔 Later: call MoMo API here
        messages.success(request, "Payment request sent. Approve on your phone.")
        return redirect('payment_status', payment.id)

    return render(request, 'payments/momo_pay.html', {'order': order})

@login_required
def payment_status(request, payment_id):    
    payment = get_object_or_404(Payment, id=payment_id, customer=request.user)

    return render(request, 'payments/payment_status.html', {'payment': payment})
