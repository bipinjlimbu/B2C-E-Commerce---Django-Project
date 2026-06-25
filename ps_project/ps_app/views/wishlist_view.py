from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Product, Wishlist

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(customer=request.user)
    return render(request, 'main/wishlist_page.html', {'wishlist_items': wishlist_items})

@login_required
def wishlist_toggle_view(request, product_id):
    product = Product.objects.get(id=product_id)
    if Wishlist.objects.filter(customer=request.user, product=product).exists():
        wishlist = Wishlist.objects.get(customer=request.user, product=product)
        wishlist.delete()
        messages.success(request, f"Product '{product.name}' has been removed from your wishlist.")
    else:
        Wishlist.objects.create(customer=request.user, product=product)
        messages.success(request, f"Product '{product.name}' has been added to your wishlist.")
        
    return redirect(f'/products/{product_id}/')

@login_required
def wishlist_remove_view(request, product_id):
    product = Product.objects.get(id=product_id)
    if Wishlist.objects.filter(customer=request.user, product=product).exists():
        wishlist = Wishlist.objects.get(customer=request.user, product=product)
        wishlist.delete()
        messages.success(request, f"Product '{product.name}' has been removed from your wishlist.")
    else:
        messages.warning(request, f"Product '{product.name}' is not in your wishlist.")
        
    return redirect('/wishlist/')