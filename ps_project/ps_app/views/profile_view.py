from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User

@login_required
def profile_view(request):
    return render(request, 'main/profile_page.html')

@login_required
def edit_profile_view(request):
    errors = {}
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        profile_picture = request.FILES.get('profile_picture')

        if not username:
            errors['username'] = 'Username is required.'
        elif User.objects.filter(username=username).exclude(pk=request.user.pk).exists():
            errors['username'] = 'Username is already taken.'
            
        if not email:
            errors['email'] = 'Email is required.'
        elif User.objects.filter(email=email).exclude(pk=request.user.pk).exists():
            errors['email'] = 'Email is already registered.'
            
        if not address:
            errors['address'] = 'Address is required.'

        if errors:
            return render(request, 'main/edit_profile_page.html', {'errors': errors, 'user': request.user, 'data': request.POST})

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.phone = phone
        user.address = address
        if profile_picture:
            user.profile_picture = profile_picture
        user.save()
        
        messages.success(request, 'Profile updated successfully.')
        return redirect('/profile/')
        
    return render(request, 'main/edit_profile_page.html')