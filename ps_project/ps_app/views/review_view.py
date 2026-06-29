from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Review, Product

@login_required
def add_review_view(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    return render(request, 'main/add_review_page.html', {'product': product})