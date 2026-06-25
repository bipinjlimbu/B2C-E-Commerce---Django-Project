from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Cart, Product, CartItem

@login_required
def add_to_cart_view(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    messages.success(request, "Product added to cart.")
    return redirect('/products')

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.total_price for item in cart_items)
    return render(request, 'main/cart_page.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def increase_cart_item_quantity(request, product_id):
    cart = Cart.objects.get(customer=request.user)
    cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('/cart/')