from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Review, Product

@login_required
def add_review_view(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    
    errors = {}
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if not rating:
            errors['rating'] = 'Rating is required.'
        if not comment:
            errors['comment'] = 'Comment is required.'
            
        if errors:
            return render(request, 'main/add_review_page.html', {'product': product, 'errors': errors, 'data': request.POST})
        
        review = Review(customer=request.user, product=product, rating=rating, comment=comment)
        review.save()
        messages.success(request, 'Review added successfully.')
        return redirect(f'/products/{product_id}/')
    
    return render(request, 'main/add_review_page.html', {'product': product})