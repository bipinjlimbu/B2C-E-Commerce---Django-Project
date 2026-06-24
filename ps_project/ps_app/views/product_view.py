from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Brand, Product

@login_required
def add_product_view(request):
    brands = Brand.objects.all()
    return render(request, 'main/add_products_page.html',{'brands':brands})