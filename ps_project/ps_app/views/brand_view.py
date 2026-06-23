from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Brand

@login_required
def add_brand_view(request):
    errors = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        logo = request.FILES.get('logo')
        
        if not name:
            errors['name'] = 'Brand name is required.'
            
        if not logo:
            errors['logo'] = 'Brand logo is required.'
            
        if errors:
            return render(request, 'main/add_brands_page.html', {'data':request.POST, 'errors': errors})
        
        brand = Brand(name=name, logo=logo)
        brand.save()
        
        messages.success(request, 'Brand added successfully.')
        return redirect('/dashboard/admin/?section=brand-management')
        
        
        
        
    return render(request, 'main/add_brands_page.html')