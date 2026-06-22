from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def add_brand_view(request):
    return render(request, 'main/add_brands_page.html')