from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Cart, Product

@login_required
def add_to_cart_view(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(customer=request.user, product = product )
    messages.success(request, "Product added to cart.")
    return redirect('/products')