from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User, Brand,Product

@login_required
def admin_dashboard_view(request):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access the admin dashboard.")
        return redirect('/')
    
    section = request.GET.get('section', 'customer-list')
    
    context = {
        'section' : section,
    }
    
    if section == 'customer-list':
        context['customers'] = User.objects.filter(is_staff=False).order_by('-date_joined')
        
    elif section == 'product-management':
        context['products'] = Product.objects.all().order_by('-created_at')
        
    elif section == 'brand-management':
        context['brands'] = Brand.objects.all()

    elif section == 'order-fulfillment':
        context['orders'] = None
        
    elif section == 'product-reviews':
        context['product_reviews'] = None
        
    elif section == 'revenue-logs':
        context['revenue_logs'] = None
        
    return render(request, 'dashboard/admin_dashboard.html', context)