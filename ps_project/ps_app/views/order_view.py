from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Order

@login_required
def order_confirmed_view(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    
    if order.customer != request.user:
        messages.error(request, 'You are not authorized to view this order.')
        return redirect('/dashboard/customer/?section=orders')
    
    if order.status == Order.Status.DELIVERED:
        order.status = Order.Status.COMPLETED
        order.save()
    else:
        messages.warning(request, 'Order is not yet delivered. Please wait for delivery confirmation.')
        return redirect('/dashboard/customer/?section=pending-orders')
    
    return redirect('/dashboard/customer/?section=my-orders')