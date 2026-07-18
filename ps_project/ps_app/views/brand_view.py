from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Brand

@login_required
def add_brand_view(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to add a brand.')
        return redirect('/dashboard/admin/?section=brand-management')
    
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

@login_required
def edit_brand_view(request, brand_id):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit a brand.')
        return redirect('/dashboard/admin/?section=brand-management')
    
    try:
        brand = Brand.objects.get(id=brand_id)
    except Brand.DoesNotExist:
        messages.error(request, 'Brand not found.')
        return redirect('/dashboard/admin/?section=brand-management')
    
    errors = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        logo = request.FILES.get('logo')
        
        if not name:
            errors['name'] = 'Brand name is required.'
            
        if not logo and not brand.logo:
            errors['logo'] = 'Brand logo is required.'
            
        if errors:
            return render(request, 'main/edit_brands_page.html', {'brand': brand, 'data': request.POST, 'errors': errors})
        
        brand.name = name
        if logo:
            brand.logo = logo
        brand.save()
        
        messages.success(request, 'Brand updated successfully.')
        return redirect('/dashboard/admin/?section=brand-management')
    
    return render(request, 'main/edit_brands_page.html', {'brand': brand})

@login_required
def delete_brand_view(request, brand_id):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete a brand.')
        return redirect('/dashboard/admin/?section=brand-management')
    
    try:
        brand = Brand.objects.get(id=brand_id)
        brand.delete()
        messages.success(request, 'Brand deleted successfully.')
    except Brand.DoesNotExist:
        messages.error(request, 'Brand not found.')
    
    return redirect('/dashboard/admin/?section=brand-management')