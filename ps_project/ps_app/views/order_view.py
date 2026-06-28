from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Order

@login_required
def order_dispatch_view(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    
    if not request.user.is_staff:
        messages.error(request, 'You are not authorized to dispatch this order.')
        return redirect('/dashboard/?section=order-fulfillment')
    
    if order.status == Order.Status.PAID:
        order.status = Order.Status.SHIPPING
        order.save()
        messages.success(request, 'Order has been dispatched successfully.')
    else:
        messages.warning(request, 'Order cannot be dispatched at this stage.')
    
    return redirect('/dashboard/?section=order-fulfillment')

@login_required
def order_confirmed_view(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    
    if order.customer != request.user:
        messages.error(request, 'You are not authorized to view this order.')
        return redirect('/dashboard/?section=orders')
    
    if order.status == Order.Status.DELIVERED:
        order.status = Order.Status.COMPLETED
        order.save()
    else:
        messages.warning(request, 'Order is not yet delivered. Please wait for delivery confirmation.')
        return redirect('/dashboard/?section=pending-orders')
    
    return redirect('/dashboard/?section=my-orders')

@login_required
def order_cancelled_view(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    
    if order.customer != request.user:
        messages.error(request, 'You are not authorized to cancel this order.')
        return redirect('/dashboard/?section=orders')
    
    if order.status in [Order.Status.PAID, Order.Status.SHIPPING]:
        order.status = Order.Status.CANCELLED
        order.save()
        
        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()
            
        messages.success(request, 'Order has been cancelled successfully.')
    else:
        messages.warning(request, 'Order cannot be cancelled at this stage.')
    
    return redirect('/dashboard/?section=my-orders')